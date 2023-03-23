disableTelemetry()

if (db.getMongo().getDBNames().indexOf("trip_offer_test_mongo") != -1) {
    db = db.getSiblingDB("trip_offer_test_mongo")
    db.dropDatabase()
}

db = db.getSiblingDB("trip_offer_test_mongo")

if (db.getUser("trip_offer_test")) {
  db.dropUser("trip_offer_test")
}

if (db.getUser("trip_offer_test_readonly")) {
  db.dropUser("trip_offer_test_readonly")
}

db.createUser({user: "trip_offer_test", pwd: "trip_offer_test", roles: [{role: "readWrite", db: "trip_offer_test_mongo"}]})
db.createUser({user: "trip_offer_test_readonly", pwd: "trip_offer_test", roles: [{role: "read", db: "trip_offer_test_mongo"}]})

db.example.createIndex(
    {"uniq_id": 1},
    {unique: true}
)