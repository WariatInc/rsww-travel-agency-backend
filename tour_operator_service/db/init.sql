DROP database if EXISTS tour_operator_pg;
CREATE database tour_operator_pg;

DROP USER if EXISTS "179919_tour_operator";
CREATE USER "179919_tour_operator" WITH password 'tour_operator';
GRANT ALL ON database tour_operator_pg TO "179919_tour_operator";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO "179919_tour_operator";

