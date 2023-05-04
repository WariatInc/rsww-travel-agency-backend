DROP database if EXISTS tour_operator_pg;
CREATE database tour_operator_pg;

DROP USER if EXISTS tour_operator;
CREATE USER "tour_operator" WITH password 'tour_operator';
GRANT ALL ON database tour_operator_pg TO tour_operator;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO tour_operator;

/* no tour_operator_readonly? */