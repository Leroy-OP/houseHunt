from django.db import migrations

AMENITIES = AMENITIES = [
    ("WiFi",                  "fas fa-wifi"),
    ("Parking",               "fas fa-car"),
    ("Swimming Pool",         "fas fa-swimming-pool"),
    ("Gym / Fitness Center",  "fas fa-dumbbell"),
    ("Air Conditioning",      "fas fa-snowflake"),
    ("Security / CCTV",       "fas fa-shield-alt"),
    ("Backup Generator",      "fas fa-bolt"),
    ("Water Supply (24hr)",   "fas fa-tint"),
    ("Elevator / Lift",       "fas fa-elevator"),
    ("Balcony",               "fas fa-building"),
    ("Garden / Yard",         "fas fa-leaf"),
    ("Furnished",             "fas fa-couch"),
    ("Pet Friendly",          "fas fa-paw"),
    ("Laundry / Washer",      "fas fa-soap"),
    ("Borehole",              "fas fa-water"),
    ("Solar Power",           "fas fa-solar-panel"),
    ("Wheelchair Accessible", "fas fa-wheelchair"),
    ("DSTV / Cable TV",       "fas fa-tv"),
    ("Storage Room",          "fas fa-box"),
    ("Rooftop Access",        "fas fa-building"),
]
    

def seed_amenities(apps, schema_editor):
    Amenity = apps.get_model("listings", "Amenity")
    for name, icon in AMENITIES:
        Amenity.objects.get_or_create(name=name, defaults={"icon": icon})

def reverse_amenities(apps, schema_editor):
    Amenity = apps.get_model("listings", "Amenity")
    Amenity.objects.filter(name__in=[n for n, _ in AMENITIES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0007_alter_amenity_name"),  # ← we'll fix this in Step 3
    ]

    operations = [
        migrations.RunPython(seed_amenities, reverse_amenities),
    ]