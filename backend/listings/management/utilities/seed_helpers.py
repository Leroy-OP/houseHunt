import random
from faker import Faker

fake = Faker()

LOCATION_WEIGHTS = {
    "Tumaini, Ongata Rongai": 25,
    "Masai Lodge, Ongata Rongai": 25,
    "Ole Kasasi, Ongata Rongai": 20,
    "Meya Road, Ongata Rongai": 15,
    "Khandisi, Ongata Rongai": 10,
    "Quarry, Ongata Rongai": 3,
    "Mandazi Road": 2,
}

PROPERTY_TYPE_WEIGHTS = {
    "studio": 30,
    "bedsitter": 40,
    "single_room": 15,
    "one_bedroom": 10,
    "two_bedroom": 5,
}

STATUS_WEIGHTS = {
    "available": 80,
    "pending": 15,
    "booked": 5,
}

PRICE_RANGES = {
    "studio": (30000, 80000),
    "bedsitter": (40000, 100000),
    "single_room": (25000, 60000),
    "one_bedroom": (50000, 120000),
    "two_bedroom": (80000, 200000),
}

FEATURES = [
    "24/7 security",
    "backup generator",
    "high-speed elevators",
    "modern fitted kitchen",
    "spacious balcony",
    "ample parking",
    "gym access",
    "proximity to public transport",
]


def weighted_choice(weight_map):
    return random.choices(
        list(weight_map.keys()),
        weights=list(weight_map.values()),
        k=1
    )[0]


def generate_title(property_type, location):
    styles = ["Modern", "Luxury", "Spacious", "Elegant", "Contemporary"]
    return f"{random.choice(styles)} {property_type.title()} in {location.split(',')[0]}"


def generate_description():
    return (
        f"{fake.paragraph(nb_sentences=4)} "
        f"Features include {random.choice(FEATURES)}, "
        f"{random.choice(FEATURES)}, and natural lighting throughout. "
        f"Ideal for modern urban living."
    )


def generate_price(property_type, location):
    base_min, base_max = PRICE_RANGES[property_type]
    base = random.randint(base_min, base_max)

    if "Masai Lodge" in location or "Tumaini" in location:
        base *= 1.3
    elif "Khandisi" in location or "Meya Road" in location:
        base *= 1.6
    elif "Quarry" in location:
        base *= 0.9

    return int(base * random.uniform(0.95, 1.05))


def image_count(property_type):
    return {
        "studio": 3,
        "single_room": 4,
        "one_bedroom": 5,
        "two_bedroom": 5,
        "bedsitter": 8,
    }[property_type]