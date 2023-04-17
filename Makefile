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

deploy: run_rabbitmq init_rabbitmq_exchange to_service res_service ## Deploy all services

deploy_full: run_rabbitmq init_rabbitmq_exchange to_db to_service res_db res_service ## Deploy all services with db initialization

run_rabbitmq: 
	docker-compose up -d --no-recreate rabbitmq

init_rabbitmq_exchange:
	sleep 10
	docker exec -it rabbitmq rabbitmqadmin declare exchange name=example type=fanout -u rabbitmq_admin -p rabbitmq

to_db:
	$(MAKE) -C ./trip_offer_service -f ./Makefile init_db

to_service:
	$(MAKE) -C ./trip_offer_service -f ./Makefile run_api_daemon

res_db:
	$(MAKE) -C ./reservation_service -f ./Makefile init_db

res_service:
	$(MAKE) -C ./reservation_service -f ./Makefile run_api_daemon

ALL_CONTAINERS_IDS := $(shell docker ps -aq)

clean: 
	docker stop $(ALL_CONTAINERS_IDS) && docker rm $(ALL_CONTAINERS_IDS)

list_container_networks:
	docker container inspect $(ALL_CONTAINERS_IDS) --format '{{json .NetworkSettings.Networks}}'
