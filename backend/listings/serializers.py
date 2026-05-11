from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Agency, Property, Booking, PropertyImage, Amenity

User = get_user_model()

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Amenity
        fields = ['id', 'name', 'icon']



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



class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Agency
        fields = '__all__'


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


class PropertySerializer(serializers.ModelSerializer):

    amenities     = AmenitySerializer(many=True, read_only=True)
    agency_detail = AgencySerializer(source='agency', read_only=True)

    images = PropertyImageSerializer(many=True, read_only=True)


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

    def create(self, validated_data):
        request   = self.context.get('request')

        amenities = validated_data.pop('amenities', [])

        instance = Property.objects.create(**validated_data)
        instance.amenities.set(amenities)
        self._handle_images(request, instance, replace=False)

        return instance


    def update(self, instance, validated_data):
        request   = self.context.get('request')

    
        amenities = validated_data.pop('amenities', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if amenities is not None:
            instance.amenities.set(amenities)

        self._handle_images(request, instance, replace=True)

        return instance

    
    def _handle_images(self, request, instance, replace: bool):
        if not request:
            return

        uploaded = request.FILES.getlist('images')
        if not uploaded:
            return

        if replace:
            
            instance.images.all().delete()

        for image_file in uploaded:
            PropertyImage.objects.create(property=instance, image=image_file)


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