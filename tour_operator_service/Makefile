PROJECT_NAME="tour_operator_service"

SHELL := bash
BASE_DIR = $(shell pwd)

STATE_DIR = .state
STATE_APP_BUILD = $(STATE_DIR)/api_build
STATE_DB_UPGRADED = $(STATE_DIR)/db_upgraded
STATE_DB_INIT = $(STATE_DIR)/db_init
STATE_DB_TEST_INIT = $(STATE_DIR)/db_test_init

DEPS_DIR = ./requirements
BASE_DEPS = $(DEPS_DIR)/base.txt
TEST_DEPS = $(DEPS_DIR)/test.txt
DEV_DEPS = $(DEPS_DIR)/dev.txt

DB_DIR = db
DB_INIT_SQL = $(DB_DIR)/init.sql
DB_TEST_INIT_SQL = $(DB_DIR)/test_init.sql
DB_DUMP = $(DB_DIR)/to_db.gz

VENV_BIN ?= python3 -m venv
VENV_DIR = venv
VENV_CFG = $(VENV_DIR)/pyvenv.cfg


PIP = $(VENV_DIR)/bin/pip
PIP_COMPILE = $(VENV_DIR)/bin/pip-compile

ISORT = $(VENV_DIR)/bin/isort
BLACK = $(VENV_DIR)/bin/black

CURRENT_MIGRATION = migrations/CURRENT

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

upgrade $(STATE_DB_UPGRADED): $(STATE_DIR) $(STATE_DB_INIT) $(STATE_API_BUILD) $(CURRENT_MIGRATION)
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator wait-for-it pg_db:5432
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator alembic upgrade head
	touch $(STATE_DB_UPGRADED)

migrate: $(STATE_DB_UPGRADED)
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator wait-for-it pg_db:5432
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator alembic revision --autogenerate --message "$(MSG)"
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator bash -c "alembic history 2>/dev/null | head -1 | cut --delimiter=' ' --fields=3,5-" > $(CURRENT_MIGRATION)

init_db $(STATE_DB_INIT): $(STATE_DIR) $(DB_INIT_SQL)
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator wait-for-it pg_db:5432
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator psql --host=pg_db --dbname=postgres --username=postgres --file=$(DB_INIT_SQL)
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator pg_restore --host=pg_db --username=tour_operator --dbname=tour_operator_pg --format=custom $(DB_DUMP)
	touch $(STATE_DB_INIT)

init_test_db $(STATE_DB_TEST_INIT): $(STATE_DIR) $(DB_TEST_INIT_SQL)
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator wait-for-it pg_db:5432
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator psql --host=pg_db --dbname=postgres --username=postgres --file=$(DB_TEST_INIT_SQL)
	touch $(STATE_DB_TEST_INIT)

build_app $(STATE_APP_BUILD): $(STATE_DIR) $(BASE_DEPS) $(TEST_DEPS) $(DEV_DEPS)
	docker-compose --project-name $(PROJECT_NAME) build tour_operator
	touch $(STATE_APP_BUILD)

run_app: $(STATE_APP_BUILD) $(STATE_DB_INIT)
	docker-compose --project-name $(PROJECT_NAME) up tour_operator

start_reservation_consumer:
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator python3 src/offer/infrastructure/message_broker/consumer.py

run_app_daemon: $(STATE_APP_BUILD) $(STATE_DB_INIT)
	docker-compose --project-name $(PROJECT_NAME) up -d --no-recreate tour_operator

psql: $(STATE_APP_BUILD)
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator psql --host=pg_db --dbname=tour_operator_pg --username=postgres

install_local: $(BASE_DEPS) $(TEST_DEPS) $(DEV_DEPS)
	$(PIP) install -r $(BASE_DEPS)
	$(PIP) install -r $(TEST_DEPS)
	$(PIP) install -r $(DEV_DEPS)

app_bash:
	docker container exec --interactive --tty $(call get_container_id, $(PROJECT_NAME)_tour_operator) bash

lint:
	$(ISORT) .
	$(BLACK) .

test: $(STATE_DB_TEST_INIT)
	docker-compose --project-name $(PROJECT_NAME) run --rm tour_operator pytest .