# Segregation Steps for Commerical Operator
&nbsp;

**Step 1: Export Commercial operator tables and data.**

Dump base tables and data required for commercial operator

```
pg_dump -U ledger_user_name -W --exclude-table='django_cron*' -t 'commercialoperator_*' -t 'django_*' -t 'taggit_*' -t 'auth_group' -t 'auth_permission' ledger_database_name > EXPORT_DIRECTORY/commercialoperator_ledger_tables.sql
```

For reversion tables only dump the schemas

```
pg_dump --schema-only -U ledger_database_name -W  -t 'reversion_*' > EXPORT_DIRECTORY/reversion_schema_commercialoperator_ledger_tables.sql
```

**Step 2 Create new commercial operator database**

As a postgres admin user (su postgres then psql) create the new commercial operator database.

CREATE DATABASE commercialoperator;

CREATE USER commercialoperator WITH PASSWORD 'password';

GRANT ALL ON DATABASE commercialoperator to commercialoperator;

\c commercialoperator

create extension postgis;

GRANT ALL ON ALL TABLES IN SCHEMA public TO commercialoperator;

GRANT ALL ON SCHEMA public TO commercialoperator;


**Step 3 Import Data into newly created database**

Import based data and tables for commercial operator.

```
psql "host=<host> port=5432 dbname=<database> user=<username> password=<password>" < EXPORT_DIRECTORY/commercialoperator_ledger_tables.sql
```

Import Base schema for reversion.

```
psql "host=<host> port=5432 dbname=<database> user=<username> password=<password>" < EXPORT_DIRECTORY/commercialoperator_ledger_tables.sql
```

**Step 4 Fix and Apply migrations**

a) Create copy of table:

```
CREATE TABLE django_migrations_temp AS SELECT * from django_migrations;
```

b). Delete Migrations in order to apply ledger_api_client migration

```
delete from django_migrations where id > 11;
```

c). Run ledger_api_client migrations

```
python manage.py migrate ledger_api_client  
```

d).  Reinsert the migrations that were deleted in step 3b.

```
insert into django_migrations (id,app,name,applied) select * from  django_migrations_temp  where id > 11;
```

e).  Delete django cron migrations so they can be created from initial migration.

```
delete from django_migrations where app = 'django_cron';
```

f).   Apply the rest of the migrations

```
python manage.py migrate
```

**Step 5 Migrate Auth Admin Group**

```
python manage.py migrate_auth_groups
```
