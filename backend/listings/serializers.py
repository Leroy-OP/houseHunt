from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Agency, Property, Booking, PropertyImage, Amenity

User = get_user_model()


# =========================
# AMENITY
# =========================

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Amenity
        fields = ['id', 'name', 'icon']


# =========================
# USER
# =========================

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'password', 'first_name']

    def create(self, validated_data):
        # Pass password directly into create_user — it handles hashing.
        # Never call set_password afterwards; that double-hashes and breaks login.
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


# =========================
# AGENCY
# =========================

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Agency
        fields = '__all__'


# =========================
# PROPERTY IMAGE
# =========================

class PropertyImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model  = PropertyImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None


# =========================
# PROPERTY
# =========================

class PropertySerializer(serializers.ModelSerializer):

    # ---- read-only nested representations ----
    amenities     = AmenitySerializer(many=True, read_only=True)
    agency_detail = AgencySerializer(source='agency', read_only=True)

    # 'images' matches related_name='images' on PropertyImage — no source= needed.
    images = PropertyImageSerializer(many=True, read_only=True)

    # ---- write-only fields ----
    # Frontend sends amenity_ids=[1,2,3]; DRF maps it to validated_data['amenities']
    amenity_ids = serializers.PrimaryKeyRelatedField(
        queryset=Amenity.objects.all(),
        many=True,
        write_only=True,
        source='amenities',
        required=False,
    )
    agency_id = serializers.PrimaryKeyRelatedField(
        queryset=Agency.objects.all(),
        write_only=True,
        source='agency',
        required=False,
    )

    class Meta:
        model  = Property
        fields = [
            'id',
            'title',
            'description',
            'price',
            'location',
            'property_type',
            'bedrooms',
            'bathrooms',
            'is_available',
            'available_from',
            'status',
            'created_at',
            # read
            'agency_detail',
            'amenities',
            'images',
            # write
            'agency_id',
            'amenity_ids',
        ]
        read_only_fields = ['created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.setdefault('amenities', [])
        data.setdefault('images', [])
        return data

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------
    def create(self, validated_data):
        request   = self.context.get('request')

        # 'amenities' is populated from the amenity_ids write field
        amenities = validated_data.pop('amenities', [])

        instance = Property.objects.create(**validated_data)
        instance.amenities.set(amenities)
        self._handle_images(request, instance, replace=False)

        return instance

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------
    def update(self, instance, validated_data):
        request   = self.context.get('request')

        # amenity_ids from the request comes through as 'amenities'
        # in validated_data due to source='amenities' on the field.
        # Pop with sentinel None so we can distinguish "not sent" from "sent empty".
        amenities = validated_data.pop('amenities', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if amenities is not None:
            instance.amenities.set(amenities)

        self._handle_images(request, instance, replace=True)

        return instance

    # ------------------------------------------------------------------
    # Image helper — single source of truth for both create and update
    # ------------------------------------------------------------------
    def _handle_images(self, request, instance, replace: bool):
        if not request:
            return

        uploaded = request.FILES.getlist('images')
        if not uploaded:
            return

        if replace:
            # Use the correct related manager — related_name='images'
            instance.images.all().delete()

        for image_file in uploaded:
            PropertyImage.objects.create(property=instance, image=image_file)


# =========================
# BOOKING
# =========================

class BookingSerializer(serializers.ModelSerializer):
    property_detail = PropertySerializer(source='property', read_only=True)

    class Meta:
        model  = Booking
        fields = [
            'id',
            'property',
            'property_detail',
            'customer_name',
            'customer_phone',
            'date',
            'time',
            'created_at',
        ]
        read_only_fields = ['created_at']
        extra_kwargs = {
            'property': {'write_only': True},
        }