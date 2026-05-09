from django.db import models
from django.conf import settings


# =========================
# AGENCY
# =========================

class Agency(models.Model):
    user    = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='agency',
    )
    name    = models.CharField(max_length=255)
    email   = models.EmailField(unique=True)
    phone   = models.CharField(max_length=20)
    company = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Agencies'
        ordering = ['name']

    def __str__(self):
        return self.name


# =========================
# AMENITY
# =========================

class Amenity(models.Model):
    """
    Predefined amenity options seeded via migration.
    Add new options to AMENITY_OPTIONS and re-run the seed migration.
    """

    AMENITY_OPTIONS = [
        # (name,                  icon_key)
        ("WiFi",                  "wifi"),
        ("Parking",               "parking"),
        ("Swimming Pool",         "pool"),
        ("Gym / Fitness Center",  "gym"),
        ("Air Conditioning",      "air_conditioning"),
        ("Security / CCTV",       "security"),
        ("Backup Generator",      "generator"),
        ("Water Supply (24hr)",   "water"),
        ("Elevator / Lift",       "elevator"),
        ("Balcony",               "balcony"),
        ("Garden / Yard",         "garden"),
        ("Furnished",             "furnished"),
        ("Pet Friendly",          "pet_friendly"),
        ("Laundry / Washer",      "laundry"),
        ("Borehole",              "borehole"),
        ("Solar Power",           "solar"),
        ("Wheelchair Accessible", "accessible"),
        ("DSTV / Cable TV",       "tv"),
        ("Storage Room",          "storage"),
        ("Rooftop Access",        "rooftop"),
    ]

    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Amenities'
        ordering = ['name']

    def __str__(self):
        return self.name

    @classmethod
    def get_default_queryset(cls):
        """Returns all seeded amenities — useful in serializers or forms."""
        return cls.objects.all()


# =========================
# PROPERTY
# =========================

class Property(models.Model):

    PROPERTY_TYPES = [
        ('apartment',   'Apartment'),
        ('studio',      'Studio'),
        ('single_room', 'Single Room'),
        ('bedsitter',   'Bedsitter'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending',   'Pending'),
        ('rented',    'Rented'),
    ]

    # Core info
    title         = models.CharField(max_length=255)
    description   = models.TextField()
    location      = models.CharField(max_length=255)
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES,
        default='apartment',
    )
    bedrooms      = models.IntegerField(default=1)
    bathrooms     = models.IntegerField(default=1)

    # Availability
    is_available   = models.BooleanField(default=True)
    available_from = models.DateField(null=True, blank=True)
    status         = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
    )

    # Relations
    agency    = models.ForeignKey(
        Agency,
        on_delete=models.CASCADE,
        related_name='properties',
    )
    amenities = models.ManyToManyField(
        Amenity,
        blank=True,
        related_name='properties',
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# =========================
# PROPERTY IMAGE
# =========================

class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(upload_to='property/')

    def __str__(self):
        return f"Image for {self.property.title}"


# =========================
# BOOKING
# =========================

class Booking(models.Model):
    property       = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    customer_name  = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=50)
    date           = models.DateField()
    time           = models.TimeField()
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (
            f"Booking by {self.customer_name} "
            f"for {self.property.title} on {self.date} at {self.time}"
        )


# =========================
# INQUIRY
# =========================

class Inquiry(models.Model):
    property   = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='inquiries',
    )
    name       = models.CharField(max_length=255)
    email      = models.EmailField()
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} about {self.property.title}"