# rsww-travel-agency-backend

In order to run all services please create ```.env.dev``` file in directories listed below. 
#
Sample ```payment_service/.env.dev``` file: 
```
FLASK_DEBUG=true
FLASK_APP=app_wsgi.py
NO_WSGI=true
PG_USER=179919_payment
PG_PASSWORD=payment
PG_DB=rsww_179919_payment
PG_HOST=pg_db
PG_PORT=5432
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=payment_user
RABBITMQ_PASSWORD=password
```

Sample ```reservation_service/.env.dev``` file: 
```
FLASK_DEBUG=true
FLASK_APP=app_wsgi.py
NO_WSGI=true
PG_USER=179919_reservation
PG_PASSWORD=reservation
PG_DB=rsww_179919_reservation
PG_HOST=pg_db
PG_PORT=5432
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=reservation_user
RABBITMQ_PASSWORD=password
```

Sample ```tour_operator_service/.env.dev``` file: 
```
FLASK_DEBUG=true
FLASK_APP=app_wsgi.py
NO_WSGI=true
PG_USER=179919_tour_operator
PG_PASSWORD=tour_operator
PG_DB=rsww_179919_tour_operator
PG_HOST=pg_db
PG_PORT=5432
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=tour_operator_user
RABBITMQ_PASSWORD=password
```

Sample ```trip_offer_service/.env.dev``` file: 

```
FLASK_DEBUG=false
FLASK_ENV=production
FLASK_APP=app_wsgi.py
NO_WSGI=true
MONGO_USER=179919_trip_offer
MONGO_PASSWORD=trip_offer
MONGO_DB=trip_offer_mongo
MONGO_HOST=mongo_db
MONGO_PORT=27017
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=trip_offer_user
RABBITMQ_PASSWORD=password
```

Sample ```api_gateway/.env.dev``` file: 
```
FLASK_DEBUG=true
FLASK_ENV=development
FLASK_APP=app_wsgi.py
NO_WSGI=true
PG_USER=179919_api_gateway
PG_PASSWORD=api_gateway
PG_DB=rsww_179919_api_gateway
PG_HOST=pg_db
PG_PORT=5432
RESERVATION_SERVICE_ROOT_URL=http://reservation_api:8000/api
PAYMENT_SERVICE_ROOT_URL=http://payment_api:8030/api
TRIP_OFFER_SERVICE_ROOT_URL=http://trip_offer_api:8010/api
```
#
In order to enusre proper DB bootstraping, please do the following steps:

- Download reservation_db.gz file from https://drive.google.com/drive/folders/1s0jmDl2_rqTmGFAQXpZk6-dPGAuXQa2P into `reservation_service/db/` folder.
- Download to_db.gz file from https://drive.google.com/drive/folders/1s0jmDl2_rqTmGFAQXpZk6-dPGAuXQa2P into `tour_operator_service/db/` folder.
- Download zip folder from https://drive.google.com/file/d/1i07d8anl8i4g2i2F0N-W9Roch2hL2qxW/view?usp=share_link
into `trip_offer_service/db/dump/` folder and extract it.
#
Please run the command in root directory:

```sudo make deploy_full```