deploy: run_rabbitmq to_service res_service

run_rabbitmq: 
	docker-compose up -d --no-recreate rabbitmq

to_service:
	$(MAKE) -C ./trip_offer_service -f ./Makefile run_api_daemon

res_service:
	$(MAKE) -C ./reservation_service -f ./Makefile run_api_daemon
