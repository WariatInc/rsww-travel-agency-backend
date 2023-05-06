DROP database if EXISTS api_gateway_test_pg;
CREATE database api_gateway_test_pg;

DROP USER if EXISTS api_gateway_test;
CREATE USER api_gateway_test WITH password 'api_gateway_test';
GRANT ALL ON database api_gateway_test_pg TO api_gateway_test;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON tables TO api_gateway_test;

DROP USER if EXISTS api_gateway_test_readonly;
CREATE USER api_gateway_test_readonly WITH password 'api_gateway_test';
GRANT CONNECT ON database api_gateway_test_pg TO api_gateway_test_readonly;
GRANT USAGE ON SCHEMA public TO api_gateway_test_readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON tables TO api_gateway_test_readonly;