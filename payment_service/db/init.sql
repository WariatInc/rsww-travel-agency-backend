DROP database if EXISTS payment_pg;
CREATE database payment_pg;

DROP USER if EXISTS payment;
CREATE USER "payment" WITH password 'payment';
GRANT ALL ON database payment_pg TO payment;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO payment;

DROP USER if EXISTS payment_readonly;
CREATE USER "payment_readonly" WITH password 'payment';
GRANT CONNECT ON DATABASE payment_pg TO payment_readonly;
GRANT pg_read_all_data TO payment_readonly;