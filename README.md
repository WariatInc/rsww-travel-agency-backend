# rsww-travel-agency-backend

In order to run all services please create ```.env.dev``` file in ```reservation_service/``` and ```trip_offer__service/``` directories. 
#
Sample ```reservation_service/.env.dev``` file: 
```
FLASK_DEBUG=true
FLASK_APP=app_wsgi.py
NO_WSGI=true
PG_USER=reservation
PG_PASSWORD=reservation
PG_DB=reservation_pg
PG_HOST=pg_db
PG_PORT=5432
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=rabbitmq_admin
RABBITMQ_PASSWORD=rabbitmq
```

Sample ```trip_offer_service/.env.dev``` file: 

```
FLASK_DEBUG=true
FLASK_APP=app_wsgi.py
NO_WSGI=true
MONGO_USER=trip_offer
MONGO_PASSWORD=trip_offer
MONGO_DB=trip_offer_mongo
MONGO_HOST=mongo_db
MONGO_PORT=27017
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=rabbitmq_admin
RABBITMQ_PASSWORD=rabbitmq
```
#
In order to enusre proper DB bootstraping, please do the following steps:

- Download zip folder from https://drive.google.com/file/d/1i07d8anl8i4g2i2F0N-W9Roch2hL2qxW/view?usp=share_link
into `trip_offer_service/db/dump/` folder.

#
Please run the command in root directory:

```sudo make deploy_full```