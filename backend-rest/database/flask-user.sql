-- Role: flaskuser
-- DROP ROLE IF EXISTS flaskuser;

-- You will need to generate your own password
CREATE ROLE flaskuser WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  CREATEDB
  NOCREATEROLE
  NOREPLICATION
  ENCRYPTED PASSWORD '<ENCRYPTED PASSWORD>';

GRANT pg_write_all_data TO flaskuser WITH ADMIN OPTION;