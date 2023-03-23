disableTelemetry()

if (db.getMongo().getDBNames().indexOf("trip_offer_mongo") != -1) {
    db = db.getSiblingDB("trip_offer_mongo")
    db.dropDatabase()
}

db = db.getSiblingDB("trip_offer_mongo")

if (db.getUser("trip_offer")) {
  db.dropUser("trip_offer")
}

if (db.getUser("trip_offer_readonly")) {
  db.dropUser("trip_offer_readonly")
}

db.createUser({user: "trip_offer", pwd: "trip_offer", roles: [{role: "readWrite", db: "trip_offer_mongo"}]})
db.createUser({user: "trip_offer_readonly", pwd: "trip_offer", roles: [{role: "read", db: "trip_offer_mongo"}]})

db.example.createIndex(
    {"uniq_id": 1},
    {unique: true}
)
