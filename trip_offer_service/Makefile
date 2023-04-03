PROJECT_NAME="trip_offer_service"

SHELL := bash
BASE_DIR = $(shell pwd)

STATE_DIR = .state
STATE_API_BUILD = $(STATE_DIR)/api_build
STATE_DB_INIT = $(STATE_DIR)/db_init
STATE_TEST_DB_INIT = $(STATE_DIR)/db_test_init

DEPS_DIR = ./requirements
BASE_DEPS = $(DEPS_DIR)/base.txt
TEST_DEPS = $(DEPS_DIR)/test.txt
DEV_DEPS = $(DEPS_DIR)/dev.txt

VENV_BIN ?= python3 -m venv
VENV_DIR = venv
VENV_CFG = $(VENV_DIR)/pyvenv.cfg

PIP = $(VENV_DIR)/bin/pip
PIP_COMPILE = $(VENV_DIR)/bin/pip-compile

DB_DIR = db
DB_INIT_JS = $(DB_DIR)/init.js
DB_TEST_INIT_JS = $(DB_DIR)/test_init.js

ISORT = $(VENV_DIR)/bin/isort
BLACK = $(VENV_DIR)/bin/black

get_container_id = $$(docker container ls | grep $(1) | cut -c1-12)


$(STATE_DIR):
	mkdir $(STATE_DIR)

$(VENV_CFG):
	$(VENV_BIN) $(VENV_DIR)

$(PIP): $(VENV_CFG)
	$(PIP) install --upgrade pip

$(PIP_COMPILE): $(PIP)
	$(PIP) install --upgrade pip-tools

$(BASE_DEPS): %.txt: %.in $(PIP_COMPILE)
	$(PIP_COMPILE) --quiet --no-emit-index-url --no-header --resolver=backtracking --strip-extras --output-file $@ $<

$(TEST_DEPS): %.txt: %.in $(BASE_DEPS)
	$(PIP_COMPILE) --quiet --no-emit-index-url --no-header --resolver=backtracking --strip-extras --output-file $@ $<

$(DEV_DEPS): %.txt: %.in $(PIP_COMPILE) $(BASE_DEPS)
	$(PIP_COMPILE) --quiet --no-emit-index-url --no-header --resolver=backtracking --strip-extras --output-file $@ $<

deps: $(BASE_DEPS) $(TEST_DEPS) $(DEV_DEPS)

build_api $(STATE_API_BUILD): $(STATE_DIR) $(BASE_DEPS) $(TEST_DEPS) $(DEV_DEPS)
	docker-compose --project-name $(PROJECT_NAME) build trip_offer_api
	touch $(STATE_API_BUILD)

init_db $(STATE_DB_INIT): $(STATE_API_BUILD) $(DB_INIT_JS)
	docker-compose --project-name $(PROJECT_NAME) run --rm trip_offer_api wait-for-it mongo_db:27017
	docker-compose --project-name $(PROJECT_NAME) run --rm trip_offer_api mongosh --host=mongo_db --port=27017 --username=mongodb_admin --password=mongodb --authenticationDatabase="admin" --file=$(DB_INIT_JS)
	touch $(STATE_DB_INIT)

init_test_db $(STATE_TEST_DB_INIT): $(STATE_API_BUILD)  $(DB_TEST_INIT_JS)
	docker-compose --project-name $(PROJECT_NAME) run --rm trip_offer_api wait-for-it mongo_db:27017
	docker-compose --project-name $(PROJECT_NAME) run --rm trip_offer_api mongosh --host=mongo_db --port=27017 --username=mongodb_admin --password=mongodb --authenticationDatabase="admin" --file=$(DB_TEST_INIT_JS)
	touch $(STATE_TEST_DB_INIT)

run_api: $(STATE_DB_INIT) $(STATE_TEST_DB_INIT)
	docker-compose --project-name $(PROJECT_NAME) up trip_offer_api

install_local: $(BASE_DEPS) $(TEST_DEPS) $(DEV_DEPS)
	$(PIP) install -r $(BASE_DEPS)
	$(PIP) install -r $(TEST_DEPS)
	$(PIP) install -r $(DEV_DEPS)

mongosh: $(STATE_API_BUILD)
	docker-compose --project-name $(PROJECT_NAME) run --rm trip_offer_api mongosh --host=mongo_db --port=27017 --username=mongodb_admin --password=mongodb trip_offer_mongo --authenticationDatabase="admin"

api_bash:
	docker container exec --interactive --tty $(call get_container_id, $(PROJECT_NAME)_trip_offer_api) bash

lint:
	$(ISORT) .
	$(BLACK) .

test: $(STATE_DB_TEST_INIT)
	docker-compose --project-name $(PROJECT_NAME) run --rm trip_offer_api pytest .
