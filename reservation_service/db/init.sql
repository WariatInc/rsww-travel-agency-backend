DROP database if EXISTS rsww_179919_reservation;
CREATE database rsww_179919_reservation;

DROP USER if EXISTS "179919_reservation";
CREATE USER "179919_reservation" WITH password 'reservation';

DROP USER if EXISTS "179919_reservation_readonly";
CREATE USER "179919_reservation_readonly" WITH password 'reservation';
