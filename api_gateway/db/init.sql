DROP database if EXISTS rsww_179919_api_gateway;
CREATE database rsww_179919_api_gateway;

DROP USER if EXISTS "179919_api_gateway";
CREATE USER "179919_api_gateway" WITH password 'api_gateway';
GRANT ALL ON database rsww_179919_api_gateway TO "179919_api_gateway";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO "179919_api_gateway";

DROP USER if EXISTS "179919_api_gateway_readonly";
CREATE USER "179919_api_gateway_readonly" WITH password 'payment';
GRANT CONNECT ON DATABASE rsww_179919_api_gateway TO "179919_api_gateway_readonly";
GRANT USAGE ON SCHEMA public TO "179919_api_gateway_readonly";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "179919_api_gateway_readonly";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO "179919_api_gateway_readonly";