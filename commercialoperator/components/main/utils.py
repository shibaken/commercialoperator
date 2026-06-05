import json
import pytz
from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.db.models import Q
from rest_framework import serializers
from ledger_api_client.ledger_models import EmailUserRO as EmailUser

import re
import os

def remove_html_tags(text):

    if text is None:
        return None

    HTML_TAGS_WRAPPED = re.compile(r'<[^>]+>.+</[^>]+>')
    HTML_TAGS_NO_WRAPPED = re.compile(r'<[^>]+>')

    text = HTML_TAGS_WRAPPED.sub('', text)
    text = HTML_TAGS_NO_WRAPPED.sub('', text)
    return text

def remove_script_tags(text):

    if text is None:
        return None

    SCRIPT_TAGS_WRAPPED = re.compile(r'(?i)<script[^>]+>.+</script[^>]+>')
    SCRIPT_TAGS_NO_WRAPPED = re.compile(r'(?i)<script[^>]+>')

    text = SCRIPT_TAGS_WRAPPED.sub('', text)
    text = SCRIPT_TAGS_NO_WRAPPED.sub('', text)

    ATTR_BLACKLIST = ['onresize','onvolumechange','onsuspend','onpopstate','onbeforeunload','oncontextmenu',
        'ondragstart','oncuechange','onselect','onafterprint','onmouseover','ondragleave','onstorage',
        'onbeforeprint','onhashchange','onabort','ondragover','onwaiting','onclick','onmousemove','onkeyup',
        'onmousedown','ononline','onsearch','onprogress','onfocus','onmouseup','onplaying','onstalled','oninvalid',
        'ontimeupdate','onkeypress','onseeked','onreset','onwheel','onemptied','oninput','onpagehide','onpause',
        'onloadeddata','onseeking','onunload','onpageshow','onerror','ondrop','oncanplay','oncopy','onended','oncut',
        'onsubmit','ondrag','onblur','ondragend','onplay','onratechange','onloadedmetadata','oncanplaythrough',
        'ondurationchange','onchange','ondblclick','onmousewheel','onpaste','onload','onscroll','onkeydown',
        'ontoggle','onmouseout','onoffline','onloadstart','ondragenter']
    ATTR_BLACKLIST_STR=('|').join(ATTR_BLACKLIST)

    HTML_TAGS_WITH_ATTR_WRAPPED = re.compile(r'(?i)<[^>]+('+ATTR_BLACKLIST_STR+')[\\s]*=[^>]+>.+</[^>]+>')
    HTML_TAGS_WITH_ATTR_NO_WRAPPED = re.compile(r'(?i)<[^>]+('+ATTR_BLACKLIST_STR+')[\\s]*=[^>]+>')

    text = HTML_TAGS_WITH_ATTR_WRAPPED.sub('', text)
    text = HTML_TAGS_WITH_ATTR_NO_WRAPPED.sub('', text)

    return text

def is_json(value):
    try:
        json.loads(value)
    except:
        return False
    return True

def sanitise_fields(instance, exclude=[], error_on_change=[]):
    if hasattr(instance,"__dict__"):
        for i in instance.__dict__:
            #remove html tags for all string fields not in the exclude list
            if not i in exclude and (isinstance(instance.__dict__[i], dict)):
                instance.__dict__[i] = sanitise_fields(instance.__dict__[i])
            
            elif isinstance(instance.__dict__[i], list) and not i in exclude:
                for j in range(0, len(instance.__dict__[i])):
                    check = instance.__dict__[i][j]
                    if isinstance(instance.__dict__[i][j],str):
                        instance.__dict__[i][j] = remove_html_tags(instance.__dict__[i][j])
                    elif isinstance(instance.__dict__[i][j], list) or isinstance(instance.__dict__[i][j], dict):
                        instance.__dict__[i][j] = sanitise_fields(instance.__dict__[i][j])
                    if i in error_on_change and check != instance.__dict__[i][j]:
                        raise serializers.ValidationError("html tags included in field")
            
            elif isinstance(instance.__dict__[i], str) and not i in exclude:
                check = instance.__dict__[i]
                setattr(instance, i, remove_html_tags(instance.__dict__[i]))
                if i in error_on_change and check != instance.__dict__[i]:
                    #only fields that cannot be allowed to change through sanitisation just before saving will throw an error
                    raise serializers.ValidationError("html tags included in field")
            elif isinstance(instance.__dict__[i], str) and i in exclude:
                check = instance.__dict__[i]
                #even though excluded, we still check to remove script tags
                setattr(instance, i, remove_script_tags(instance.__dict__[i]))
                if i in error_on_change and check != instance.__dict__[i]:
                    #only fields that cannot be allowed to change through sanitisation just before saving will throw an error
                    raise serializers.ValidationError("script tags included in field")
            elif (isinstance(instance.__dict__[i], list) or isinstance(instance.__dict__[i], dict)) and i in exclude:
                #if we have reached this point, it means we have a json object with fields that are allowed to contain tags
                #we'll use . notation to identify sub fields that should be carried over to the exclude and error on change lists
                #NOTE: to allow sub fields to be sanitised, the parent field should be included in both lists required for their respective children
                sub_exclude_list = list(filter(lambda e:e.startswith(i+"."), exclude))
                exclude_list = list(map(lambda e:e.replace(i+".","",1), sub_exclude_list))
                #NOTE: a sub error on change list will require the parent field to be in the exclude list, to reach this point (but not necessarily in the error_on_change list)
                sub_error_on_change_list = list(filter(lambda e:e.startswith(i+"."), error_on_change))
                error_on_change_list = list(map(lambda e:e.replace(i+".","",1), sub_error_on_change_list))

                if isinstance(instance.__dict__[i], dict):
                    check = instance.__dict__[i]
                    instance.__dict__[i] = sanitise_fields(instance.__dict__[i], exclude=exclude_list, error_on_change=error_on_change_list)
                    if i in error_on_change and check != instance.__dict__[i]:
                        raise serializers.ValidationError("html tags included in field")
                elif isinstance(instance.__dict__[i], list):
                    for j in range(0, len(instance.__dict__[i])):
                        check = instance.__dict__[i][j]
                        if isinstance(instance.__dict__[i][j],str):
                            #strings in an excluded list will be treated as excluded
                            instance.__dict__[i][j] = remove_script_tags(instance.__dict__[i][j])
                        elif isinstance(instance.__dict__[i][j], list) or isinstance(instance.__dict__[i][j], dict):
                            instance.__dict__[i][j] = sanitise_fields(instance.__dict__[i][j], exclude=exclude_list, error_on_change=error_on_change_list)
                        if i in error_on_change and check != instance.__dict__[i][j]:
                            raise serializers.ValidationError("html tags included in field")
    else:
        remove_keys = []
        for i in instance:
            #for dicts we also check the keys - they are removed completely if not sanitary (should not change keys)
            original_key = i
            if isinstance(original_key, str):
                sanitised_key = remove_html_tags(i)
                if original_key != sanitised_key:
                    remove_keys.append(original_key)
                    continue

            #remove html tags for all string fields not in the exclude list
            if not i in exclude and (isinstance(instance[i], dict)):
                instance[i] = sanitise_fields(instance[i])

            elif isinstance(instance[i], list) and not i in exclude:
                for j in range(0, len(instance[i])):
                    check = instance[i][j]
                    if isinstance(instance[i][j],str):
                        instance[i][j] = remove_html_tags(instance[i][j])
                    elif isinstance(instance[i][j], list) or isinstance(instance[i][j], dict):
                        instance[i][j] = sanitise_fields(instance[i][j])
                    if i in error_on_change and check != instance[i][j]:
                        raise serializers.ValidationError("html tags included in field")

            else:
                if isinstance(instance[i], str) and not i in exclude:
                    check = instance[i]
                    instance[i] = remove_html_tags(instance[i])
                    if i in error_on_change and check != instance[i]:
                        #only fields that cannot be allowed to change through sanitisation just before saving will throw an error
                        raise serializers.ValidationError("html tags included in field")
                elif isinstance(instance[i], str) and i in exclude:
                    #even though excluded, we still check to remove script tags
                    instance[i] = remove_script_tags(instance[i])
                    if i in error_on_change and check != instance[i]:
                        #only fields that cannot be allowed to change through sanitisation just before saving will throw an error
                        raise serializers.ValidationError("script tags included in field")
                elif (isinstance(instance[i], list) or isinstance(instance[i], dict)) and i in exclude:
                    #if we have reached this point, it means we have a json object with fields that are allowed to contain tags
                    #we'll use . notation to identify sub fields that should be carried over to the exclude and error on change lists
                    #NOTE: to allow sub fields to be sanitised, the parent field should be included in both lists required for their respective children
                    sub_exclude_list = list(filter(lambda e:e.startswith(i+"."), exclude))
                    exclude_list = list(map(lambda e:e.replace(i+".","",1), sub_exclude_list))
                    #NOTE: a sub error on change list will require the parent field to be in the exclude list, to reach this point (but not necessarily in the error_on_change list)
                    sub_error_on_change_list = list(filter(lambda e:e.startswith(i+"."), error_on_change))
                    error_on_change_list = list(map(lambda e:e.replace(i+".","",1), sub_error_on_change_list))

                    if isinstance(instance[i], dict):
                        check = instance[i]
                        instance[i] = sanitise_fields(instance[i], exclude=exclude_list, error_on_change=error_on_change_list)
                        if i in error_on_change and check != instance[i]:
                            raise serializers.ValidationError("script tags included in field")
                    elif isinstance(instance[i], list):                        
                        for j in range(0, len(instance[i])):
                            check = instance[i][j]
                            if isinstance(instance[i][j],str):
                                #strings in an excluded list will be treated as excluded
                                instance[i][j] = remove_script_tags(instance[i][j])
                            elif isinstance(instance[i][j], list) or isinstance(instance[i][j], dict):
                                instance[i][j] = sanitise_fields(instance[i][j], exclude=exclude_list, error_on_change=error_on_change_list)
                            if i in error_on_change and check != instance[i][j]:
                                raise serializers.ValidationError("script tags included in field")
                    
        for i in remove_keys:
            del instance[i]
    return instance

def file_extension_valid(file, whitelist, model):
    _, extension = os.path.splitext(file)
    extension = extension.replace(".", "").lower()

    check = whitelist.filter(name=extension).filter(
        Q(model="all") | Q(model__iexact=model)
    )
    valid = check.exists()

    return valid

def check_file(file, model_name):
    from commercialoperator.components.main.models import FileExtensionWhitelist

    # check if extension in whitelist
    cache_key = settings.CACHE_KEY_FILE_EXTENSION_WHITELIST
    whitelist = cache.get(cache_key)
    if whitelist is None:
        whitelist = FileExtensionWhitelist.objects.all()
        cache.set(cache_key, whitelist, settings.CACHE_TIMEOUT_2_HOURS)

    valid = file_extension_valid(str(file), whitelist, model_name)

    if not valid:
        raise serializers.ValidationError("File type/extension not supported")
    

def get_department_user(email):
    if (EmailUser.objects.filter(email__iexact=email.strip()) and 
            EmailUser.objects.get(email__iexact=email.strip()).is_staff):
        return True
    return False

def to_local_tz(_date):
    local_tz = pytz.timezone(settings.TIME_ZONE)
    return _date.astimezone(local_tz)

def check_db_connection():
    """  check connection to DB exists, connect if no connection exists """
    try:
        if not connection.is_usable():
            connection.connect()
    except Exception as e:
        connection.connect()