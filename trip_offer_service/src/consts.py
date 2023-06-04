from src.enum import StrEnum, auto


class Exchanges(StrEnum):
    example = auto()
    offer = auto()


class Queues(StrEnum):
    trip_offer_service_offer_queue = auto()


class Collections(StrEnum):
    tour = "Tour"
    offer = "Offer"
    offer_view = "OfferView"


class TransportType(StrEnum):
    self = auto()
    bus = auto()
    plane = auto()


class RoomType(StrEnum):
    standard = auto()
    family = auto()
    apartment = auto()
    studio = auto()


class KidsAgeRange(StrEnum):
    up_to_3 = auto()
    up_to_10 = auto()
    up_to_18 = auto()


AVERAGE_NIGHT_COST_PER_COUNTRY = {
    "Albania": 100,
    "Aruba": 300,
    "Austria": 200,
    "Bali": 1000,
    "Bułgaria": 70,
    "Chorwacja": 90,
    "Cypr": 150,
    "Czarnogóra": 50,
    "Czechy": 60,
    "Dominikana": 400,
    "Egipt": 60,
    "Estonia": 40,
    "Francja": 200,
    "Grecja": 100,
    "Gruzja": 60,
    "Hiszpania": 150,
    "Indonezja - Bali": 500,
    "Jamajka": 500,
    "Kenia": 140,
    "Kuba": 150,
    "Litwa": 50,
    "Macedonia": 80,
    "Madera": 140,
    "Malediwy": 600,
    "Malta": 200,
    "Maroko": 230,
    "Meksyk": 140,
    "Niemcy": 150,
    "Oman": 90,
    "Polska": 140,
    "Portugalia": 180,
    "Rumunia": 70,
    "Serbia": 80,
    "Sri Lanka": 240,
    "Szwajcaria": 160,
    "Słowacja": 90,
    "Słowenia": 90,
    "Tajlandia": 70,
    "Tunezja": 70,
    "Turcja": 75,
    "Wielka Brytania": 180,
    "Wyspy Kanaryjskie": 200,
    "Wyspy Zielonego Przylądka": 200,
    "Węgry": 90,
    "Włochy": 190,
    "Zanzibar": 300,
    "Zjednoczone Emiraty Arabskie": 190,
    "Łotwa": 80,
}


AVERAGE_FLIGHT_COST_PER_COUNTRY = {
    "Albania": 300,
    "Aruba": 1900,
    "Austria": 70,
    "Bali": 2500,
    "Bułgaria": 200,
    "Chorwacja": 200,
    "Cypr": 300,
    "Czarnogóra": 150,
    "Czechy": 150,
    "Dominikana": 1200,
    "Egipt": 500,
    "Estonia": 200,
    "Francja": 300,
    "Grecja": 500,
    "Gruzja": 300,
    "Hiszpania": 400,
    "Indonezja - Bali": 2000,
    "Jamajka": 2400,
    "Kenia": 1700,
    "Kuba": 2300,
    "Litwa": 130,
    "Macedonia": 600,
    "Madera": 500,
    "Malediwy": 600,
    "Malta": 200,
    "Maroko": 400,
    "Meksyk": 2000,
    "Niemcy": 250,
    "Oman": 900,
    "Polska": 30,
    "Portugalia": 400,
    "Rumunia": 300,
    "Serbia": 330,
    "Sri Lanka": 1400,
    "Szwajcaria": 400,
    "Słowacja": 150,
    "Słowenia": 350,
    "Tajlandia": 2000,
    "Tunezja": 750,
    "Turcja": 500,
    "Wielka Brytania": 200,
    "Wyspy Kanaryjskie": 500,
    "Wyspy Zielonego Przylądka": 800,
    "Węgry": 250,
    "Włochy": 250,
    "Zanzibar": 2300,
    "Zjednoczone Emiraty Arabskie": 1000,
    "Łotwa": 400,
}


ROOM_TYPE_MULTIPLIER = {
    RoomType.standard: 1,
    RoomType.family: 1.5,
    RoomType.studio: 0.75,
    RoomType.apartment: 2.5,
}


KIDS_HOTEL_DISCOUNT = {
    KidsAgeRange.up_to_3: 0.1,
    KidsAgeRange.up_to_10: 0.5,
    KidsAgeRange.up_to_18: 0.8,
}

KIDS_FLIGHT_DISCOUNT = {
    KidsAgeRange.up_to_3: 0.0,
    KidsAgeRange.up_to_10: 0.6,
    KidsAgeRange.up_to_18: 0.85,
}


PROVISION = 0.1
