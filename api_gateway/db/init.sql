DROP database if EXISTS api_gateway_pg;
CREATE database api_gateway_pg;

DROP USER if EXISTS "179919_api_gateway";
CREATE USER "179919_api_gateway" WITH password 'api_gateway';
GRANT ALL ON database api_gateway_pg TO "179919_api_gateway";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO "179919_api_gateway";
