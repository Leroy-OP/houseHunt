import os
import time
import random
import requests
from django.core.management.base import BaseCommand
from listings.models import Property, Agency, PropertyImage
from dotenv import load_dotenv

from listings.management.utilities.seed_helpers import (
    weighted_choice,
    LOCATION_WEIGHTS,
    PROPERTY_TYPE_WEIGHTS,
    STATUS_WEIGHTS,
    generate_title,
    generate_description,
    generate_price,
    image_count,
)

load_dotenv()

UNSPLASH_KEY = os.getenv("UNSPLASH_KEY", "").strip()

# Fallback images (used if API fails)
FALLBACK_IMAGES = [
    "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688",
    "https://images.unsplash.com/photo-1493809842364-78817add7ffb",
    "https://images.unsplash.com/photo-1484154218962-a197022b5858",
    "https://images.unsplash.com/photo-1507089947367-19c1da9775ae",
]

def get_image(query):
    """
    Fetch ONE image from Unsplash safely
    """
    if not UNSPLASH_KEY:
        return random.choice(FALLBACK_IMAGES)

    url = "https://api.unsplash.com/photos/random"

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_KEY}",
        "Accept-Version": "v1",
    }

    params = {
        "query": query,
        "orientation": "landscape",
    }

    for attempt in range(3):
        try:
            res = requests.get(url, headers=headers, params=params, timeout=10)
            res.raise_for_status()
            return res.json()["urls"]["regular"]

        except requests.exceptions.RequestException as e:
            print(f"[Retry {attempt+1}] Error: {e}")
            time.sleep(1.5)

    return random.choice(FALLBACK_IMAGES)


class Command(BaseCommand):
    help = "Seed realistic property data with images"

    def handle(self, *args, **kwargs):

        if not UNSPLASH_KEY:
            self.stdout.write(self.style.WARNING("⚠ No Unsplash key — using fallback images only"))

        agency, _ = Agency.objects.get_or_create(
            name="Default Agency",
            defaults={
                "email": "default@example.com",
                "phone": "0000000000",
            },
        )

        Property.objects.filter(agency=agency).delete()

    
        self.stdout.write("Fetching image pool...")

        image_pool = []
        base_queries = [
            "apartment interior",
            "modern house interior",
            "living room design",
            "bedroom interior",
            "kitchen modern",
        ]

        for i in range(30):  # ONLY 30 API calls total
            query = random.choice(base_queries)
            image_pool.append(get_image(query))
            time.sleep(0.5)  # prevents rate limiting

        # fallback safety
        if not image_pool:
            image_pool = FALLBACK_IMAGES

        # ✅ STEP 2: Create properties
        self.stdout.write("Creating properties...")

        for _ in range(50):

            location = weighted_choice(LOCATION_WEIGHTS)
            property_type = weighted_choice(PROPERTY_TYPE_WEIGHTS)
            status = weighted_choice(STATUS_WEIGHTS)

            prop = Property.objects.create(
                title=generate_title(property_type, location),
                description=generate_description(),
                location=location,
                price=generate_price(property_type, location),
                property_type=property_type,
                agency=agency,
            )

            count = image_count(property_type)

            selected_images = random.sample(
                image_pool,
                min(count, len(image_pool))
            )

            for img in selected_images:
                PropertyImage.objects.create(
                    property=prop,
                    image_url=img,
                )

        self.stdout.write(self.style.SUCCESS("✅ Seed completed successfully!"))