deploy: run_rabbitmq to_service res_service ## Deploy all services

deploy_full: run_rabbitmq to_db to_service res_db res_service ## Deploy all services with db initialization

run_rabbitmq: 
	docker-compose up -d --no-recreate rabbitmq

to_db:
	$(MAKE) -C ./trip_offer_service -f ./Makefile init_db

to_service:
	$(MAKE) -C ./trip_offer_service -f ./Makefile run_api_daemon

res_db:
	$(MAKE) -C ./reservation_service -f ./Makefile init_db

res_service:
	$(MAKE) -C ./reservation_service -f ./Makefile run_api_daemon
