DROP database if EXISTS tour_operator_test_pg;
CREATE database tour_operator_test_pg;

DROP USER if EXISTS tour_operator_test;
CREATE USER "tour_operator_test" WITH password 'tour_operator_test';
GRANT ALL ON database tour_operator_test_pg TO tour_operator_test;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO tour_operator_test;
