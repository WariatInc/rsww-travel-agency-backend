DROP database if EXISTS reservation_pg;
CREATE database reservation_pg;

DROP USER if EXISTS reservation;
CREATE USER "reservation" WITH password 'reservation';
GRANT ALL ON database reservation_pg TO reservation;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO reservation;

DROP USER if EXISTS reservation_readonly;
CREATE USER "reservation_readonly" WITH password  'reservation';
GRANT CONNECT ON DATABASE reservation_pg TO reservation_readonly;
GRANT USAGE ON SCHEMA public TO reservation_readonly;
GRANT SELECT ON ALL tables IN SCHEMA public TO reservation_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON tables TO reservation_readonly;