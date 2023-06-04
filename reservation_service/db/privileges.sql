GRANT ALL ON database rsww_179919_reservation TO "179919_reservation";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO "179919_reservation";

GRANT CONNECT ON DATABASE rsww_179919_reservation TO "179919_reservation_readonly";
GRANT USAGE ON SCHEMA public TO "179919_reservation_readonly";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "179919_reservation_readonly";
ALTER DEFAULT PRIVILEGES FOR ROLE "179919_reservation_readonly" IN SCHEMA public GRANT SELECT ON TABLES TO "179919_reservation_readonly";
