DROP database if EXISTS rsww_179919_tour_operator;
CREATE database rsww_179919_tour_operator;

DROP USER if EXISTS "179919_tour_operator";
CREATE USER "179919_tour_operator" WITH password 'tour_operator';
GRANT ALL ON database rsww_179919_tour_operator TO "179919_tour_operator";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO "179919_tour_operator";

