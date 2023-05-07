DROP database if EXISTS api_gateway_pg;
CREATE database api_gateway_pg;

DROP USER if EXISTS api_gateway;
CREATE USER "api_gateway" WITH password 'api_gateway';
GRANT ALL ON database api_gateway_pg TO api_gateway;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO api_gateway;

DROP USER if EXISTS api_gateway_readonly;
CREATE USER "api_gateway_readonly" WITH password 'api_gateway';
GRANT CONNECT ON DATABASE api_gateway_pg TO api_gateway_readonly;
GRANT pg_read_all_data TO api_gateway_readonly;