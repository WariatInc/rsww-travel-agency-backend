DROP database if EXISTS payment_pg;
CREATE database payment_pg;

DROP USER if EXISTS "179919_payment";
CREATE USER "179919_payment" WITH password 'payment';
GRANT ALL ON database payment_pg TO "179919_payment";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO "179919_payment";

DROP USER if EXISTS "179919_payment_readonly";
CREATE USER "179919_payment_readonly" WITH password 'payment';
GRANT CONNECT ON DATABASE payment_pg TO "179919_payment_readonly";
GRANT USAGE ON SCHEMA public TO "179919_payment_readonly";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "179919_payment_readonly";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "179919_payment_readonly";