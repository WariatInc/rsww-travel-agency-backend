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

deploy: run_rabbitmq init_rabbitmq_exchange payment_service reservation_service tour_operator_service trip_offer_service ## Deploy all services

deploy_full: run_rabbitmq init_rabbitmq_exchange payment_db payment_service reservation_db reservation_service tour_operator_db tour_operator_service trip_offer_db trip_offer_service ## Deploy all services with db initialization

run_rabbitmq: 
	docker-compose up -d --no-recreate rabbitmq

init_rabbitmq_exchange:
	sleep 10

	docker exec -it rabbitmq rabbitmqctl add_user trip_offer_user password
	docker exec -it rabbitmq rabbitmqctl add_user reservation_user password
	docker exec -it rabbitmq rabbitmqctl add_user tour_operator_user password
	docker exec -it rabbitmq rabbitmqctl add_user payment_user password

	docker exec -it rabbitmq rabbitmqctl set_permissions -p / trip_offer_user ".*" ".*" ".*"
	docker exec -it rabbitmq rabbitmqctl set_permissions -p / reservation_user ".*" ".*" ".*"
	docker exec -it rabbitmq rabbitmqctl set_permissions -p / tour_operator_user  ".*" ".*" ".*"
	docker exec -it rabbitmq rabbitmqctl set_permissions -p / payment_user  ".*" ".*" ".*"

	docker exec -it rabbitmq rabbitmqctl set_user_tags trip_offer_user management
	docker exec -it rabbitmq rabbitmqctl set_user_tags reservation_user management
	docker exec -it rabbitmq rabbitmqctl set_user_tags tour_operator_user management
	docker exec -it rabbitmq rabbitmqctl set_user_tags payment_user management

	docker exec -it rabbitmq rabbitmqadmin declare exchange name=offer type=fanout -u rabbitmq_admin -p rabbitmq
	docker exec -it rabbitmq rabbitmqadmin declare exchange name=reservation type=fanout -u rabbitmq_admin -p rabbitmq
	docker exec -it rabbitmq rabbitmqadmin declare exchange name=payment type=fanout -u rabbitmq_admin -p rabbitmq

	docker exec -it rabbitmq rabbitmqadmin declare queue name=tour_operator_reservation_queue durable=true -u rabbitmq_admin -p rabbitmq
	docker exec -it rabbitmq rabbitmqadmin declare queue name=reservation_service_reservation_queue durable=true -u rabbitmq_admin -p rabbitmq
	docker exec -it rabbitmq rabbitmqadmin declare queue name=reservation_service_payment_queue durable=true -u rabbitmq_admin -p rabbitmq
	docker exec -it rabbitmq rabbitmqadmin declare queue name=payment_service_reservation_queue durable=true -u rabbitmq_admin -p rabbitmq

	docker exec -it rabbitmq rabbitmqadmin declare binding source="reservation" destination_type="queue" destination="tour_operator_reservation_queue" routing_key="" -u rabbitmq_admin -p rabbitmq
	docker exec -it rabbitmq rabbitmqadmin declare binding source="reservation" destination_type="queue" destination="reservation_service_reservation_queue" routing_key="" -u rabbitmq_admin -p rabbitmq
	docker exec -it rabbitmq rabbitmqadmin declare binding source="reservation" destination_type="queue" destination="payment_service_reservation_queue" routing_key="" -u rabbitmq_admin -p rabbitmq
	docker exec -it rabbitmq rabbitmqadmin declare binding source="payment" destination_type="queue" destination="reservation_service_payment_queue" routing_key="" -u rabbitmq_admin -p rabbitmq

payment_db:
	$(MAKE) -C ./payment_service -f ./Makefile init_db

payment_service:
	$(MAKE) -C ./payment_service -f ./Makefile run_api_daemon

reservation_db:
	$(MAKE) -C ./reservation_service -f ./Makefile init_db

reservation_service:
	$(MAKE) -C ./reservation_service -f ./Makefile run_api_daemon

tour_operator_db:
	$(MAKE) -C ./tour_operator_service -f ./Makefile init_db

tour_operator_service:
	$(MAKE) -C ./tour_operator_service -f ./Makefile run_api_daemon

trip_offer_db:
	$(MAKE) -C ./trip_offer_service -f ./Makefile init_db

trip_offer_service:
	$(MAKE) -C ./trip_offer_service -f ./Makefile run_api_daemon

ALL_CONTAINERS_IDS := $(shell docker ps -aq)

clean: 
	docker stop $(ALL_CONTAINERS_IDS) && docker rm $(ALL_CONTAINERS_IDS)

list_container_networks:
	docker container inspect $(ALL_CONTAINERS_IDS) --format '{{json .NetworkSettings.Networks}}'
