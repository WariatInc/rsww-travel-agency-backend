DROP database if EXISTS payment_test_pg;
CREATE database payment_test_pg;

DROP USER if EXISTS payment_test;
CREATE USER payment_test WITH password 'payment_test';
GRANT ALL ON database payment_test_pg TO payment_test;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO payment_test;

DROP USER if EXISTS payment_test_readonly;
CREATE USER payment_test_readonly WITH password 'payment_test';
GRANT CONNECT ON database payment_test_pg TO payment_test_readonly;
GRANT USAGE ON SCHEMA public TO payment_test_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON tables TO payment_test_readonly;