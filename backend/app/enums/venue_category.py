from enum import Enum


class VenueCategory(str, Enum):
    BAR = "BAR"
    RESTAURANT = "RESTAURANT"
    CLUB = "CLUB"
    CAFE = "CAFE"
    ROOFTOP = "ROOFTOP"
    SHOPPING = "SHOPPING"
    ENTERTAINMENT = "ENTERTAINMENT"
    PARC = "PARC"
    SPORT = "SPORT"