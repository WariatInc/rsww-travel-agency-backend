# Copyright (c) 2023 WariatInc
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

deploy: run_rabbitmq \
        init_rabbitmq_exchange \
		run_postgres \
		run_mongo \
		payment_service \
		reservation_service \
		tour_operator_service \
		trip_offer_service ## Deploy all services

deploy_full: run_rabbitmq \
			 init_rabbitmq_exchange \
			 run_postgres \
			 configure_payment_db \
			 deploy_payment_service \
			 configure_reservation_db \
			 deploy_reservation_service \
			 configure_tour_operator_db \
			 deploy_tour_operator_service \
			 run_mongo \
			 configure_trip_offer_db \
			 deploy_trip_offer_service \
			 run_bootstrap_mongo \
			 configure_api_gateway_db \
			 deploy_api_gateway  ## Deploy all services with db initialization

deploy_consumers:
			 start_payment_service_reservation_consumer \
			 start_reservation_service_reservation_consumer \
			 start_reservation_service_payment_consumer \
			 start_tour_operator_service_reservation_consumer \
			 start_trip_offer_service_offer_consumer

run_postgres: 
	docker-compose up -d --no-recreate pg_db

run_mongo: 
	docker-compose up -d --no-recreate mongo_db

run_bootstrap_mongo:
	$(MAKE) -C ./trip_offer_service -f ./Makefile bootstrap_db

run_rabbitmq: 
	docker-compose up -d --no-recreate rabbitmq

init_rabbitmq_exchange:
	sleep 10

	docker-compose exec rabbitmq rabbitmqctl add_user trip_offer_user password
	docker-compose exec rabbitmq rabbitmqctl add_user reservation_user password
	docker-compose exec rabbitmq rabbitmqctl add_user tour_operator_user password
	docker-compose exec rabbitmq rabbitmqctl add_user payment_user password

	docker-compose exec rabbitmq rabbitmqctl set_permissions -p / trip_offer_user ".*" ".*" ".*"
	docker-compose exec rabbitmq rabbitmqctl set_permissions -p / reservation_user ".*" ".*" ".*"
	docker-compose exec rabbitmq rabbitmqctl set_permissions -p / tour_operator_user  ".*" ".*" ".*"
	docker-compose exec rabbitmq rabbitmqctl set_permissions -p / payment_user  ".*" ".*" ".*"

	docker-compose exec rabbitmq rabbitmqctl set_user_tags trip_offer_user management
	docker-compose exec rabbitmq rabbitmqctl set_user_tags reservation_user management
	docker-compose exec rabbitmq rabbitmqctl set_user_tags tour_operator_user management
	docker-compose exec rabbitmq rabbitmqctl set_user_tags payment_user management

	docker-compose exec rabbitmq rabbitmqadmin declare exchange name=offer type=fanout -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare exchange name=reservation type=fanout -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare exchange name=payment type=fanout -u rabbitmq_admin -p rabbitmq

	docker-compose exec rabbitmq rabbitmqadmin declare queue name=tour_operator_reservation_queue durable=true -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare queue name=reservation_service_reservation_queue durable=true -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare queue name=reservation_service_payment_queue durable=true -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare queue name=payment_service_reservation_queue durable=true -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare queue name=trip_offer_service_offer_queue durable=true -u rabbitmq_admin -p rabbitmq

	docker-compose exec rabbitmq rabbitmqadmin declare binding source="reservation" destination_type="queue" destination="tour_operator_reservation_queue" routing_key="" -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare binding source="reservation" destination_type="queue" destination="reservation_service_reservation_queue" routing_key="" -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare binding source="reservation" destination_type="queue" destination="payment_service_reservation_queue" routing_key="" -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare binding source="payment" destination_type="queue" destination="reservation_service_payment_queue" routing_key="" -u rabbitmq_admin -p rabbitmq
	docker-compose exec rabbitmq rabbitmqadmin declare binding source="offer" destination_type="queue" destination="trip_offer_service_offer_queue" routing_key="" -u rabbitmq_admin -p rabbitmq

configure_payment_db:
	$(MAKE) -C ./payment_service -f ./Makefile init_db

deploy_payment_service:
	$(MAKE) -C ./payment_service -f ./Makefile run_api_daemon

configure_reservation_db:
	$(MAKE) -C ./reservation_service -f ./Makefile init_db

deploy_reservation_service:
	$(MAKE) -C ./reservation_service -f ./Makefile run_api_daemon

configure_tour_operator_db:
	$(MAKE) -C ./tour_operator_service -f ./Makefile init_db

deploy_tour_operator_service:
	$(MAKE) -C ./tour_operator_service -f ./Makefile run_app_daemon

configure_trip_offer_db:
	$(MAKE) -C ./trip_offer_service -f ./Makefile init_db

deploy_trip_offer_service:
	$(MAKE) -C ./trip_offer_service -f ./Makefile run_api_daemon

configure_api_gateway_db:
	$(MAKE) -C ./api_gateway -f ./Makefile init_db

deploy_api_gateway:
	$(MAKE) -C ./api_gateway -f ./Makefile run_api_daemon

start_payment_service_reservation_consumer:
	$(MAKE) -C ./payment_service -f ./Makefile start_reservation_consumer_daemon

start_reservation_service_reservation_consumer:
	$(MAKE) -C ./reservation_service -f ./Makefile start_reservation_consumer_daemon

start_reservation_service_payment_consumer:
	$(MAKE) -C ./reservation_service -f ./Makefile start_payment_consumer_daemon

start_tour_operator_service_reservation_consumer:
	$(MAKE) -C ./tour_operator_service -f ./Makefile start_reservation_consumer_daemon

start_trip_offer_service_offer_consumer:
	$(MAKE) -C ./trip_offer_service -f ./Makefile start_offer_consumer_daemon

ALL_CONTAINERS_IDS := $(shell docker ps -aq)

clean: 
	docker stop $(ALL_CONTAINERS_IDS) && docker rm $(ALL_CONTAINERS_IDS)

list_container_networks:
	docker container inspect $(ALL_CONTAINERS_IDS) --format '{{json .NetworkSettings.Networks}}'
