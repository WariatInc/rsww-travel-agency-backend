DROP database if EXISTS rsww_179919_reservation;
CREATE database rsww_179919_reservation;

DROP USER if EXISTS "179919_reservation";
CREATE USER "179919_reservation" WITH password 'reservation';
GRANT ALL ON database rsww_179919_reservation TO "179919_reservation";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO "179919_reservation";

DROP USER if EXISTS "179919_reservation_readonly";
CREATE USER "179919_reservation_readonly" WITH password 'reservation';
GRANT CONNECT ON DATABASE rsww_179919_reservation TO "179919_reservation_readonly";
GRANT USAGE ON SCHEMA public TO "179919_reservation_readonly";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "179919_reservation_readonly";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "179919_reservation_readonly";
