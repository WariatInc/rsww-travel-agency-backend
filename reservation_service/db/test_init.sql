DROP database if EXISTS reservation_test_pg;
CREATE database reservation_test_pg;

DROP USER if EXISTS reservation_test;
CREATE USER "reservation_test" WITH password 'reservation_test';
GRANT ALL ON database reservation_test_pg TO reservation_test;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO reservation_test;

DROP USER if EXISTS reservation_test_readonly;
CREATE USER "reservation_test_readonly" WITH password 'reservation_test';
GRANT CONNECT ON database reservation_test_pg TO reservation_test_readonly;
GRANT USAGE ON SCHEMA public TO reservation_test_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON tables TO reservation_test_readonly;


