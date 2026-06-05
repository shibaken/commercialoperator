from itertools import islice, chain

from django.apps import apps
from django.db import models, connection
from django.conf import settings
from django.core.cache import cache
from rest_framework import status

from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from typing import Iterable, Mapping, Optional, Sequence
from django.db.models import QuerySet
from ledger_api_client.utils import (
    create_basket_session as ledger_create_basket_session,
    oracle_parser as ledger_oracle_parser,
    update_payments as ledger_update_payments,
    get_all_organisation,
    get_organisation,
    get_search_organisation,
)
from ledger_api_client.common import get_ledger_user_info_by_id

from typing import override

import logging

from commercialoperator.components.segregation.decorators import log_execution_time
from commercialoperator.components.segregation.mixins import (
    FilterHelperMixin,
    RecursiveGetAttributeMixin,
)

logger = logging.getLogger(__name__)


def retrieve_email_user(email_user_id):
    if not email_user_id:
        logger.error("Needs an email_user_id to retrieve an EmailUser object")
        return None

    if isinstance(email_user_id, EmailUser):
        #logger.warning(
        #    f"Retrieved EmailUser object {email_user_id} directly. Returning."
        #)
        return email_user_id

    cache_key = settings.CACHE_KEY_LEDGER_EMAIL_USER.format(email_user_id)
    cache_timeout = settings.CACHE_TIMEOUT_10_SECONDS
    email_user = cache.get(cache_key)

    if email_user is None:
        try:
            email_user = EmailUser.objects.get(id=email_user_id)
        except EmailUser.DoesNotExist:
            logger.error(f"EmailUser with id {email_user_id} does not exist")
            # Cache an empty EmailUser object to prevent repeated queries
            cache.set(cache_key, EmailUser(), cache_timeout)
            return None
        except TypeError:
            logger.error(
                f"Type {type(email_user_id)} `email_user_id` parameter {email_user_id} must be an integer."
            )
            raise TypeError(
                f"Type {type(email_user_id)} `email_user_id` parameter {email_user_id} must be an integer."
            )
        else:
            cache.set(cache_key, email_user, cache_timeout)
            return email_user
    elif not email_user.email:
        return None
    else:
        return email_user


def retrieve_email_user_by_email(email):
    """
    Retrieves an EmailUser object by email address.
    Args:
        email (str): The email address of the user.
    Returns:
        EmailUser: The EmailUser object if found, None otherwise.
    """
    if not email:
        logger.error("Needs an email to retrieve an EmailUser object")
        return None

    cache_key = settings.CACHE_KEY_LEDGER_EMAIL_USER_BY_EMAIL.format(email)
    cache_timeout = settings.CACHE_TIMEOUT_10_SECONDS
    email_user = cache.get(cache_key)

    if email_user is None:
        try:
            email_user = EmailUser.objects.get(email=email)
        except EmailUser.DoesNotExist:
            logger.error(f"EmailUser with email {email} does not exist")
            # Cache an empty EmailUser object to prevent repeated queries
            cache.set(cache_key, EmailUser(), cache_timeout)
            return None
        else:
            cache.set(cache_key, email_user, cache_timeout)
            return email_user
    else:
        return email_user


def retrieve_organisation(organisation_id):
    if not organisation_id:
        logger.error(
            "Needs an organisation_id to retrieve a Ledger Organisation object"
        )
        return None

    cache_key = settings.CACHE_KEY_LEDGER_ORGANISATION.format(organisation_id)
    cache_timeout = settings.CACHE_TIMEOUT_5_MINUTES
    organisation = cache.get(cache_key)

    if organisation is None:
        organisation_response = get_organisation(organisation_id)
        if organisation_response.get("status", None) != status.HTTP_200_OK:
            return None
        else:
            organisation = organisation_response.get("data", {})
            cache.set(cache_key, organisation, cache_timeout)
            return organisation
    else:
        return organisation


def rgetattr(obj, dotted_path: str, *, raise_exception: bool = False):
    """
    Recursive getattr using dot-notation (e.g., 'foo.bar.baz').
    Works for Django related objects that are already loaded.
    """
    try:
        for part in dotted_path.split('.'):
            obj = getattr(obj, part)
        return obj
    except AttributeError:
        if raise_exception:
            raise ValueError(f"Property {dotted_path} does not exist on {type(obj).__name__}")
        return None


def expand_organisation_fields(
    queryset: QuerySet,
    organisation_foreign_key_field: str,
    organisation_properties: Optional[Iterable[str]] = None,
) -> QuerySet:

    if not organisation_foreign_key_field:
        raise ValueError("organisation_foreign_key_field must be provided")

    if organisation_properties is None:
        organisation_properties = []

    # Build names used throughout
    org_fk_field_id = f"{organisation_foreign_key_field}_id"
    org_fk_field_dot = organisation_foreign_key_field.replace("__", ".")

    # Prepare structures
    ledger_org_ids: list[int] = []
    row_org_ids: list[int] = []  # local FK PKs associated with rows, used to anchor CASE
    row_property_values: dict[int, dict[str, str]] = {}

    # Pre-calculate mapping: '<ledger_object>__prop' -> list of 'prop' to read from ledger record
    # Example: 'organisation__name' -> {'organisation_id': ['name']}
    ledger_prop_map: dict[str, list[str]] = {}
    for prop in organisation_properties:
        parts = prop.split("__", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid organisation property '{prop}'. Expected '<object>__<field>'.")
        ledger_object_name, ledger_prop = parts
        ledger_id_field_name = f"{ledger_object_name}_id"
        ledger_prop_map.setdefault(ledger_id_field_name, []).append(ledger_prop)

    # Mild mitigation of N+1 on simple FK: select_related first segment
    first_segment = organisation_foreign_key_field.split("__", 1)[0]
    qs_iter = queryset.select_related(first_segment)

    # Walk rows and collect ledger org data
    for obj in qs_iter:
        # e.g. row.org_applicant or row.org_applicant.organisation
        holder = rgetattr(obj, org_fk_field_dot, raise_exception=True)

        # 'row_org_id' = PK of the holder object (row-level anchor)
        row_org_id = getattr(holder, "pk", None)

        for ledger_id_field_name, ledger_props in ledger_prop_map.items():
            # 'ledger_org_id' lives on the holder object, e.g. holder.organisation_id
            ledger_org_id = getattr(holder, ledger_id_field_name, None)
            if not ledger_org_id:
                continue

            # Retrieve ledger organisation record
            ledger_org: Mapping[str, str] | None = retrieve_organisation(ledger_org_id)
            if not ledger_org:
                logger.error("Organisation with id %s does not exist in the ledger", ledger_org_id)
                continue

            # Collect unique ledger IDs
            if ledger_org_id not in ledger_org_ids:
                ledger_org_ids.append(ledger_org_id)

            # Track row org ids for CASE anchors
            if row_org_id and row_org_id not in row_org_ids:
                row_org_ids.append(row_org_id)

            # Collect property values per-row anchor
            if row_org_id:
                vals = row_property_values.setdefault(row_org_id, {})
                for lp in ledger_props:
                    vals[lp] = ledger_org.get(lp, "")

    # Build CASE/WHEN annotations for each requested property
    case_whens: dict[str, models.Case] = {}
    for prop in organisation_properties:
        # Final field name: '<fk>_<object>_<prop>' with double underscores flattened
        annotated_field_name = f"{organisation_foreign_key_field}_{prop}".replace("__", "_")

        whens: list[models.When] = []
        for row_org_id_value in row_org_ids:
            # Property key used inside the collected dict is the LAST segment of prop
            prop_key = prop.split("__")[-1]
            prop_val = row_property_values.get(row_org_id_value, {}).get(prop_key, "")

            whens.append(
                models.When(
                    **{org_fk_field_id: row_org_id_value},
                    then=models.Value(prop_val),
                )
            )

        case_whens[annotated_field_name] = models.Case(
            *whens,
            default=models.Value(""),
            output_field=models.CharField(),
        )

    # Build 'exists' boolean annotation
    exists_field_name = f"{organisation_foreign_key_field}_exists"
    annotations = {
        exists_field_name: models.Case(
            models.When(**{f"{org_fk_field_id}__in": ledger_org_ids}, then=models.Value(True)),
            default=models.Value(False),
            output_field=models.BooleanField(),
        )
    }
    annotations.update(case_whens)

    logger.debug("Annotating queryset with organisation properties: %s", list(case_whens.keys()))
    annotated_qs = queryset.annotate(**annotations)

    return annotated_qs


def expand_emailuser_fields(queryset, emailuser_fk_field, emailuser_properties=None):
    if emailuser_properties is None:
        emailuser_properties = []

    emailuser_fk_field_id = f"{emailuser_fk_field}_id"
    emailuser_fk_field_id_dotnotation = emailuser_fk_field_id.replace("__", ".")

    emailuser_fk_field_ids = []
    emailuser_fk_field_property_values = {}

    for obj in queryset:
        emailuser_fk_field_id_value = getattr(obj, emailuser_fk_field_id, None)
        emailuser = retrieve_email_user(emailuser_fk_field_id_value) if emailuser_fk_field_id_value else None
        if emailuser:
            setattr(obj, emailuser_fk_field, emailuser)
            if emailuser.id not in emailuser_fk_field_ids:
                emailuser_fk_field_ids.append(emailuser.id)
            if emailuser.id not in emailuser_fk_field_property_values:
                emailuser_fk_field_property_values[emailuser.id] = {}
            for prop in emailuser_properties:
                emailuser_fk_field_property_values[emailuser.id][prop] = getattr(emailuser, prop)

    # Annotate queryset with Case expressions
    case_whens = {
        f"{emailuser_fk_field}_{prop}".replace("__", "_"): models.Case(
            *[
                models.When(**{emailuser_fk_field_id: id_val}, then=models.Value(emailuser_fk_field_property_values[id_val][prop]))
                for id_val in emailuser_fk_field_ids
            ],
            default=models.Value(""),
            output_field=models.CharField(),
        )
        for prop in emailuser_properties
    }

    return queryset.annotate(
        **{
            f"{emailuser_fk_field}_exists": models.Case(
                models.When(**{f"{emailuser_fk_field_id}__in": emailuser_fk_field_ids}, then=models.Value(True)),
                default=models.Value(False),
                output_field=models.BooleanField(),
            )
        }
    ).annotate(**case_whens)


def check_table_exists(table_name):
    """
    Checks if a table exists in the database.
    Args:
        table_name (str): The name of the table to check.
    Returns:
        bool: True if the table exists, False otherwise.
    """

    with connection.cursor() as cursor:
        # Check if the table exists in the database
        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)",
            [table_name],
        )
        return cursor.fetchone()[0]


class EmailUserQuerySet(models.QuerySet, RecursiveGetAttributeMixin, FilterHelperMixin):
    LEDGER_EXPAND_TARGET_EMAILUSER = "emailuser"
    LEDGER_EXPAND_TARGET_ORGANISATION = "organisation"
    LEDGER_EXPAND_TARGETS = {
        LEDGER_EXPAND_TARGET_EMAILUSER: "expand_emailuser_fields",
        LEDGER_EXPAND_TARGET_ORGANISATION: "expand_organisation_fields",
    }

    @log_execution_time
    def expand_emailuser_fields(self, emailuser_fk_field, emailuser_properties={}):
        """
        Adds the emailuser object to the QuerySet and expands it with additional fields that are properties
        of an EmailUser foreign key if provided through the `emailuser_properties` parameter.

        Args:
            emailuser_fk_field: str, name of the field that points to an EmailUser foreign key, e.g. "submitter"
            emailuser_properties: Set of str, names of the properties of EmailUser to be added to the QuerySet,
                e.g. ["email", "first_name", "last_name"] become submitter_email, submitter_first_name, submitter_last_name
                if emailuser_fk_field is "submitter"

        Returns:
            QuerySet with additional fields emailuser_fk_field_exists, emailuser_fk_field_email, emailuser_fk_field_first_name, emailuser_fk_field_last_name
        """

        if not emailuser_fk_field:
            raise ValueError(
                "A emailuser_fk_field that points to an EmailUser foreign key must be provided"
            )

        emailuser_fk_field_id = f"{emailuser_fk_field}_id"

        emailuser_fk_field_id_dotnotation = emailuser_fk_field_id.replace("__", ".")

        emailuser_fk_field_ids = []
        emailuser_fk_field_property_values = {}

        for obj in self:
            emailuser_fk_field_id_value = None
            try:
                emailuser_fk_field_id_value = self.rgetattr(
                    obj, emailuser_fk_field_id_dotnotation, raise_exception=True
                )
            except ValueError as e:
                raise ValueError(
                    f"Property {emailuser_fk_field_id_dotnotation} does not exist in the {self.model.__name__} object"
                )

            emailuser = (
                retrieve_email_user(emailuser_fk_field_id_value)
                if emailuser_fk_field_id_value
                else None
            )
            if emailuser:
                setattr(obj, emailuser_fk_field, emailuser)
                if emailuser.id not in emailuser_fk_field_ids:
                    # Collect unique emailuser ids
                    emailuser_fk_field_ids.append(emailuser.id)
                if emailuser.id not in emailuser_fk_field_property_values:
                    # Collect emailuser properties
                    emailuser_fk_field_property_values[emailuser.id] = {}
                for property in emailuser_properties:
                    # Collect emailuser property values
                    emailuser_fk_field_property_values[emailuser.id][property] = (
                        getattr(emailuser, property)
                    )

        # Create a dictionary of Case expressions for each emailuser property
        # E.g. {
        #     "submitter_email": Case(
        #         When(submitter_id=1, then=Value("email1")),
        #         When(submitter_id=2, then=Value("email2")),
        #         default=Value(""),
        #         output_field=CharField()
        #     ),
        case_whens = {
            f"{emailuser_fk_field}_{property}".replace("__", "_"): models.Case(
                *[
                    models.When(
                        **{f"{emailuser_fk_field_id}": emailuser_fk_field_id_value},
                        then=models.Value(
                            emailuser_fk_field_property_values[
                                emailuser_fk_field_id_value
                            ][property]
                        ),
                    )
                    for emailuser_fk_field_id_value in emailuser_fk_field_ids
                ],
                default=models.Value(""),
                output_field=models.CharField(),
            )
            for property in emailuser_properties
        }

        logger.debug(
            f"Annotating queryset with emailuser properties: {case_whens.keys()}"
        )
        # Add the emailuser_fk_field_exists field, e.g. submitter_exists
        self = self.annotate(
            **{
                f"{emailuser_fk_field}_exists": models.Case(
                    models.When(
                        **{f"{emailuser_fk_field_id}__in": emailuser_fk_field_ids},
                        then=models.Value(True),
                    ),
                    default=models.Value(False),
                    output_field=models.BooleanField(),
                )
            }
        ).annotate(**case_whens)

        return self

    @log_execution_time
    def expand_organisation_fields(
        self, organisation_foreign_key_field, organisation_properties={}
    ):
        if not organisation_foreign_key_field:
            raise ValueError(
                "A organisation_foreign_key_field that points to an Organisation foreign key must be provided"
            )

        organisation_foreign_key_field_id = f"{organisation_foreign_key_field}_id"
        organisation_fk_field_dotnotation = organisation_foreign_key_field.replace(
            "__", "."
        )

        ledger_organisation_ids = []
        cols_organisation_ids = []
        ledger_organisation_property_values = {}

        for obj in self:
            cols_organisation = None

            try:
                cols_organisation = self.rgetattr(
                    obj, organisation_fk_field_dotnotation, raise_exception=True
                )
            except ValueError as e:
                raise ValueError(
                    f"Property {organisation_fk_field_dotnotation} does not exist in the {self.model.__name__} object"
                )

            ledger_organisations = {}

            # @log_execution_time
            def build_ledger_organisations_dict(organisation_properties):
                for organisation_property in organisation_properties:
                    props = organisation_property.split("__")
                    ledger_object_name = props[0]
                    ledger_object_value = props[1]

                    ledger_organisation_id_name = f"{ledger_object_name}_id"

                    if ledger_organisation_id_name not in ledger_organisations:
                        ledger_organisations[ledger_organisation_id_name] = []

                    ledger_organisations[ledger_organisation_id_name] += [
                        ledger_object_value
                    ]

            build_ledger_organisations_dict(organisation_properties)

            # @log_execution_time
            def execute_ledger_retrieve_organisations():
                for (
                    ledger_organisation_id_name,
                    ledger_organisation_id_properties,
                ) in ledger_organisations.items():
                    if not ledger_organisation_id_properties:
                        continue

                    cols_organisation_id = getattr(cols_organisation, "pk", None)
                    ledger_organisation_id = getattr(
                        cols_organisation, ledger_organisation_id_name, None
                    )
                    ledger_organisation = retrieve_organisation(ledger_organisation_id)
                    if not ledger_organisation:
                        logger.error(
                            f"Organisation with id {ledger_organisation_id} does not exist in the ledger"
                        )
                        continue

                    if ledger_organisation:
                        if ledger_organisation_id not in ledger_organisation_ids:
                            # Collect unique organisation ids
                            ledger_organisation_ids.append(ledger_organisation_id)
                            cols_organisation_ids.append(cols_organisation_id)
                        if (
                            cols_organisation_id
                            not in ledger_organisation_property_values
                        ):
                            # Collect organisation properties
                            ledger_organisation_property_values[
                                cols_organisation_id
                            ] = {}
                        for property in ledger_organisation_id_properties:
                            # Collect organisation property values, associate a cols org id with ledger org values (e.g. name, email, etc.)
                            ledger_organisation_property_values[cols_organisation_id][
                                property
                            ] = ledger_organisation.get(property, "")

            execute_ledger_retrieve_organisations()

        # Create a dictionary of Case expressions for each organisation property
        # E.g. {
        #     "org_applicant_organisation_organisation_name": Case(
        #         When(org_applicant_id=1, then=Value("Organisation 1 Name")),
        #         When(org_applicant_id=2, then=Value("Organisation 2 Name")),
        #         default=Value(""),
        #         output_field=CharField()
        #     ),
        #     "org_applicant_organisation_organisation_email": Case(
        #         When(org_applicant_id=1, then=Value("Organisation 1 Email")),
        #         When(org_applicant_id=2, then=Value("Organisation 2 Email")),
        #         default=Value(""),
        #         output_field=CharField()
        #     )
        case_whens = {
            f"{organisation_foreign_key_field}_{property}".replace(
                "__", "_"
            ): models.Case(
                *[
                    models.When(
                        **{
                            f"{organisation_foreign_key_field_id}": cols_organisation_id_value
                        },
                        then=models.Value(
                            ledger_organisation_property_values[
                                cols_organisation_id_value
                            ][property.split("__")[-1]]
                        ),
                    )
                    for cols_organisation_id_value in cols_organisation_ids
                ],
                default=models.Value(""),
                output_field=models.CharField(),
            )
            for property in organisation_properties
        }

        logger.debug(
            f"Annotating queryset with organisation properties: {case_whens.keys()}"
        )
        self = self.annotate(
            **{
                f"{organisation_foreign_key_field}_exists": models.Case(
                    models.When(
                        **{
                            f"{organisation_foreign_key_field_id}__in": ledger_organisation_ids
                        },
                        then=models.Value(True),
                    ),
                    default=models.Value(False),
                    output_field=models.BooleanField(),
                )
            }
        ).annotate(**case_whens)

        return self

    def get_ledger_retrieve_function(self, field_name, ledger_lookup_extras):
        """Retrieve the appropriate ledger lookup and expand function for a given field."""

        retrieve_function_target = ledger_lookup_extras.get(
            field_name, self.LEDGER_EXPAND_TARGET_EMAILUSER
        )
        retrieve_function_name = self.LEDGER_EXPAND_TARGETS.get(
            retrieve_function_target
        )
        retrieve_function = getattr(self, retrieve_function_name, None)
        if not retrieve_function:
            raise ValueError(
                f"Invalid ledger lookup target '{retrieve_function_target}' for field '{field_name}'."
            )
        return retrieve_function

    @override
    def order_by(self, *field_names, **kwargs):
        ledger_lookup_fields = kwargs.get("ledger_lookup_fields", {})
        ledger_lookup_extras = kwargs.get("ledger_lookup_extras", {})

        if any(isinstance(f, models.Case) for f in field_names):
            # If any of the field names are Case expressions, go with default ordering
            logger.debug("Ordering by Case expressions, using default ordering.")
            return super().order_by(*field_names)

        # Check if any of the field names start with a ledger lookup field (ignoring asc or desc ordering)
        fields_by_ledger_lookup = [
            {l: f}
            for f in field_names
            for l in ledger_lookup_fields
            if f.replace("-", "").startswith(l)
        ]
        is_ledger_lookup = bool(fields_by_ledger_lookup)

        if not is_ledger_lookup:
            # If no ledger lookup fields are provided, use the default ordering

            orderings, reverse = self.to_case_insensitive_ordering(field_names, self)

            orderings_with_lower = []
            # If the ordering contains Lower functions, annotate the queryset with them
            from django.db.models.functions import Lower
            from django.db.models import F, Func

            for idx, ordering in enumerate(orderings):
                ordering = orderings[idx]
                if not isinstance(ordering, Lower):
                    # If the ordering is not a Lower function, just append it
                    orderings_with_lower.append(ordering)
                    continue
                field_name = field_names[idx]
                to_lower_field_name = f"to_lower_{field_name}"
                # If the ordering is a Lower function, annotate the queryset with it
                orderings_with_lower.append(to_lower_field_name)

                self = self.annotate(**{to_lower_field_name: ordering})
                # qs = self.annotate(**{to_lower_field_name: Func(F(field_name), function=Lower, output_field=models.CharField())})

            # Order the queryset by the annotated Lower fields
            qs = super().order_by(*orderings_with_lower)
            if reverse:
                qs = qs.reverse()
            return qs

    # Handle ledger lookup ordering logic here if needed

        # A dictionary of each ledger lookup field and its subfields
        expand_fields = {}
        for item in fields_by_ledger_lookup:
            for field_name, ledger_lookup in item.items():
                if field_name not in expand_fields:
                    expand_fields[field_name] = []
                # Add the ledger lookup to the expand fields
                ll_no_ordering = ledger_lookup.replace("-", "")
                if not ll_no_ordering.startswith(field_name):
                    # If the ledger lookup does not start with the field name, raise an error
                    raise ValueError(
                        f"Ledger lookup field '{ledger_lookup}' does not start with the field name '{field_name}'."
                    )

                ledger_lookup_property = ll_no_ordering.replace(field_name, "")
                if not ledger_lookup_property.startswith("__"):
                    # If the ledger lookup property does not start with __, raise an error
                    raise ValueError(
                        f"Ledger lookup property '{ledger_lookup_property}' does not start with '__'."
                    )
                # Remove the __ from the ledger lookup property
                ledger_lookup_property = ledger_lookup_property[2:]
                expand_fields[field_name].append(ledger_lookup_property)
                logger.debug(
                    f"Expanding field {field_name} with ledger lookup {ledger_lookup}"
                )

        # Expand the queryset with annotations in the form of submitter__email translates to submitter_email
        for key, value in expand_fields.items():
            # Emailuser or organisation (default is emailuser if not provided in the kwargs)
            retrieve_function = self.get_ledger_retrieve_function(
                key, ledger_lookup_extras
            )

            # Call the proper retrieve function with the key and value
            self = retrieve_function(key, value)

        # A list of field names that have been expanded in the prior step to order by, e.g. ["submitter_email", "submitter_first_name"] or ['-submitter_first_name', '-submitter_last_name']
        expanded_field_names = [f.replace("__", "_") for f in field_names]

        logger.debug(f"Ordering queryset by expanded fields: {expanded_field_names}")

        # Convert the expanded field names to a case-insensitive ordering
        ordering, reverse = self.to_case_insensitive_ordering(
            expanded_field_names, self
        )
        qs = super().order_by(*ordering)
        if reverse:
            qs = qs.reverse()
        return qs

    def distinct(self, *args, **kwargs):
        """
        Returns a distinct queryset based on the fields provided.
        If no fields are provided, it returns a distinct queryset based on all fields.
        """

        if not args and not kwargs:
            return super().distinct()

        distinct_fields = []
        for arg in args:
            if not self.query.annotations.get(f"to_lower_{arg}", None):
                # If the field is not annotated with a Lower function, add it directly
                distinct_fields.append(arg)
                continue
            # If the field is annotated with a Lower function, add the annotated field name
            distinct_fields.append(f"to_lower_{arg}")

        qs = super().distinct(*distinct_fields, **kwargs)

        return qs

    def values_list(self, *fields, **kwargs):
        flat = kwargs.pop("flat", False)
        _fields = list(fields) + list(self.query.annotations.keys())

        # If annotated, for some strange reason we have to include the annotated fields in the values or values_list calls
        values = self.values(*_fields)
        field_length = 1 if flat else len(fields)
        values_list_with_annotations = super(EmailUserQuerySet, values).values_list(
            *_fields, **kwargs
        )
        values_list = [v[:field_length] for v in values_list_with_annotations]
        if field_length == 1 and flat:
            # If flat is True and only one field is provided, return a flat list
            values_list = [v[0] for v in values_list]
        else:
            logger.warning("Not a flat list")

        return values_list


#TODO review the anything that "needs to be implemented with ledger api client", remove if not applicable
def createCustomBasket(*args, **kwargs):
    logger.error(ledger_create_basket_session)
    raise NotImplementedError(
        "ledger.checkout.utils.createCustomBasket needs to be implemented with ledger api client"
    )


def oracle_parser(*args, **kwargs):
    logger.error(ledger_oracle_parser)
    raise NotImplementedError(
        "ledger.payments.utils.oracle_parser needs to be implemented with ledger api client"
    )


def update_payments(*args, **kwargs):
    logger.error(ledger_update_payments)
    raise NotImplementedError(
        "ledger.payments.utils.update_payments needs to be implemented with ledger api client"
    )


def retrieve_group_members(group_object, app_label="commercialoperator"):
    """Retrieves m2m-field members that belong to a group-object (single object or queryset), using the associated through model"""

    if hasattr(group_object, "_meta"):
        # group_object is a model object
        try:
            # The group object's model name
            model_name = group_object._meta.model_name
        except AttributeError:
            raise ValueError("The model object does not have a model name attribute")
        # Get the group object's Members through-model
        class_name = f"{model_name.lower()}members"
        InstanceClass = apps.get_model(app_label=app_label, model_name=f"{class_name}")

        return InstanceClass.objects.filter(
            **{f"{model_name.lower()}_id": group_object.id}
        ).values_list("emailuser_id", flat=True)
    else:
        # group_object is a QuerySet
        class_name = group_object.model.__name__
        return group_object.values_list(
            f"{class_name.lower()}_members__emailuser__id", flat=True
        )


def retrieve_user_groups(class_name, user_id, app_label="commercialoperator"):
    """Retrieves m2m-field groups a user belongs to, using the associated through model"""

    InstanceClass = apps.get_model(app_label=app_label, model_name=f"{class_name}")

    return InstanceClass.objects.filter(
        **{f"{class_name.lower()}_members__emailuser_id": user_id}
    )


def retrieve_members(class_object, app_label="commercialoperator"):
    """Retrieves m2m-field members using the associated through model
    `ClassWithMembersFieldMembers`.
    """

    class_name = class_object.__class__.__name__
    InstanceClass = apps.get_model(
        app_label=app_label, model_name=f"{class_name}Members"
    )
    return InstanceClass.objects.filter(
        **{f"{class_name.lower()}_id": class_object.id}
    ).values_list("emailuser_id", flat=True)


def retrieve_delegate_organisation_ids(email_user_id):
    from commercialoperator.components.organisations.models import (
        Organisation,
        UserDelegation,
    )

    organisation_ids = UserDelegation.objects.filter(user_id=email_user_id).values_list(
        "organisation__organisation_id", flat=True
    )

    return organisation_ids


def retrieve_organisation_delegate_ids(organisation_id):
    from commercialoperator.components.organisations.models import (
        Organisation,
        UserDelegation,
    )

    delegate_ids = UserDelegation.objects.filter(
        organisation_id=organisation_id
    ).values_list("user_id", flat=True)

    return delegate_ids


def retrieve_ledger_user_info_by_id(email_user_id):
    """Queries ledger user info, that contains user details or information status"""

    cache_key = settings.CACHE_KEY_LEDGER_USER_INFO.format(email_user_id)
    cache_timeout = settings.CACHE_TIMEOUT_5_SECONDS

    user_info = cache.get(cache_key)

    if user_info is None:
        user_info = get_ledger_user_info_by_id(f"{email_user_id}")
        if user_info.get("status", None) != status.HTTP_200_OK:
            return {}

        cache.set(cache_key, user_info, cache_timeout)
        return user_info
    else:
        return user_info


def retrieve_cols_organisations_from_ledger_org_ids(user):
    """Takes a user object, retrieves the organisations that the user is a delegate of from the ledger
    and adds the corresponding organisation model id to the ledger organisation object.
    """

    from commercialoperator.components.organisations.models import Organisation

    user_id = user.id
    user_ledger_org_ids = retrieve_delegate_organisation_ids(user_id)

    commercialoperator_organisations = []

    for org_id in user_ledger_org_ids:

        cache_key = settings.CACHE_KEY_LEDGER_ORGANISATION.format(org_id)
        cache_timeout = settings.CACHE_TIMEOUT_5_MINUTES

        ledger_organisation = cache.get(cache_key)

        if ledger_organisation:
            # If the organisation is in the cache, use it
            logger.debug(f"Organisation {org_id} found in cache")
            commercialoperator_organisations.append(ledger_organisation)
            continue

        organisations_response = get_organisation(org_id)

        if organisations_response.get("status", None) == status.HTTP_200_OK:
            # Get the organisation object from ledger
            ledger_organisation = organisations_response.get("data", [])
            # Add the cols organisation model id to the ledger organisation object
            commercialoperator_organisation = Organisation.objects.get(
                organisation_id=org_id
            )
            ledger_organisation["id"] = commercialoperator_organisation.id
            commercialoperator_organisations.append(ledger_organisation)

            cache.set(cache_key, ledger_organisation, cache_timeout)
        else:
            raise ValueError(f"Error retrieving organisations for user {user_id}")
        logger.info(
            f"Retrieved organisations for user {user_id}: {commercialoperator_organisations}"
        )

    return commercialoperator_organisations


class ListAsQuerySet(list):

    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self


def filter_organisation_list(view, request, *args, **kwargs):
    from commercialoperator.components.segregation.models import LedgerOrganisation

    queryset = view.get_queryset()

    search_term = request.query_params.get("search", None)
    if search_term is None:
        ledger_organisation_response = get_all_organisation()
    elif search_term.isdigit():
        logger.debug("Searching for organisation ABN")
        # Function signature: get_search_organisation(organisation_name, organisation_abn)
        ledger_organisation_response = get_search_organisation(None, search_term)
    else:
        logger.debug("Searching for organisation name")
        ledger_organisation_response = get_search_organisation(search_term, None)

    if ledger_organisation_response["status"] == status.HTTP_200_OK:
        ledger_organisations = ledger_organisation_response["data"]
    else:
        logger.debug(
            f"Failed to retrieve organisations from ledger: {ledger_organisation_response.get("message", "")}"
        )
        return LedgerOrganisation.objects.none()

    org_ids = queryset.values_list("organisation_id", flat=True)

    organisation_dicts = [
        org for org in ledger_organisations if org["organisation_id"] in org_ids
    ]

    organisations = [LedgerOrganisation(**org_dict) for org_dict in organisation_dicts]
    organisations = view.filter_queryset(
        ListAsQuerySet(organisations, model=LedgerOrganisation)
    )[:10]

    return organisations


class QuerySetChain(object):
    """
    Chains multiple subquerysets (possibly of different models) and behaves as
    one queryset.  Supports minimal methods needed for use with
    django.core.paginator.
    """

    def __init__(self, *subquerysets):
        self.querysets = subquerysets

    def count(self):
        """
        Performs a .count() for all subquerysets and returns the number of
        records as an integer.
        """

        return sum(qs.count() for qs in self.querysets)

    def order_by(self, *field_names):
        """
        Returns a list of the unique ordering fields for all subquerysets.
        """
        querysets = ()
        for qs in self.querysets:
            querysets += (qs.distinct().order_by(*field_names),)

        return self.__init__(*querysets)

    def _clone(self):
        "Returns a clone of this queryset chain"

        return self.__class__(*self.querysets)

    def _all(self):
        "Iterates records in all subquerysets"

        return chain(*self.querysets)

    def __getitem__(self, ndx):
        """
        Retrieves an item or slice from the chained set of results from all
        subquerysets.
        """

        if type(ndx) is slice:
            return list(islice(self._all(), ndx.start, ndx.stop, ndx.step or 1))
        else:
            return next(islice(self._all(), ndx, ndx + 1))
