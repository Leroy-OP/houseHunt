from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

from .models import Agency, Property, Booking, PropertyImage, Amenity
from .serializers import (
    AgencySerializer,
    PropertySerializer,
    BookingSerializer,
    AmenitySerializer,
)

User = get_user_model()


@api_view(['POST'])
def register(request):
    data     = request.data
    email    = data.get('email')
    password = data.get('password')
    name     = data.get('name', '')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already registered.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        first_name=name,
    )

    return Response(
        {
            'id':      user.id,
            'email':   user.email,
            'name':    user.first_name,
            'message': 'User registered successfully.',
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
def login(request):
    email    = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # ------------------------------------------------------------------
    # Look up the user by email first, then authenticate by their actual
    # username. This handles agency accounts whose username may differ
    # from their email (e.g. created via Django admin).
    # ------------------------------------------------------------------
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    user = authenticate(request, username=user_obj.username, password=password)

    if user is None:
        return Response(
            {'error': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        'token': str(refresh.access_token),
        'user': {
            'id':    user.id,
            'email': user.email,
            'name':  user.first_name,
            'role':  getattr(user, 'role', None),
        },
    })


# =========================
# VIEWSETS
# =========================

class AgencyViewSet(viewsets.ModelViewSet):
    queryset           = Agency.objects.all()
    serializer_class   = AgencySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = (
        Property.objects
        .select_related('agency')
        .prefetch_related('amenities', 'images')
    )
    serializer_class   = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        # Pass request into serializer so image URLs can be made absolute
        # and so _handle_images can access request.FILES
        return {'request': self.request}

    # ------------------------------------------------------------------
    # Shared permission guard
    # ------------------------------------------------------------------
    def _assert_agency_owner(self, user, instance=None):
        if not user or not user.is_authenticated:
            raise PermissionDenied("Authentication required.")
        

        agency = getattr(user, 'agency', None)
        if not agency:
            raise PermissionDenied("Only agency users can manage properties.")
        if instance and instance.agency != agency:
            raise PermissionDenied("You do not own this property.")

    # ------------------------------------------------------------------
    # CREATE
    # Amenity sync is fully handled inside PropertySerializer.create()
    # via validated_data — no duplication here.
    # ------------------------------------------------------------------
    def perform_create(self, serializer):
        self._assert_agency_owner(self.request.user)
        serializer.save(agency=self.request.user.agency)

    # ------------------------------------------------------------------
    # UPDATE  (PUT / PATCH)
    # Amenity + image sync is fully handled inside PropertySerializer.update()
    # Do NOT re-sync here — that caused the PATCH amenities bug.
    # ------------------------------------------------------------------
    def perform_update(self, serializer):
        self._assert_agency_owner(self.request.user, instance=serializer.instance)
        serializer.save()

    # ------------------------------------------------------------------
    # Agency's own properties
    # ------------------------------------------------------------------
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my(self, request):
        agency = getattr(request.user, 'agency', None)

        if not agency:
            return Response(
                {'detail': 'User is not an agency account.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        properties = (
            Property.objects
            .filter(agency=agency)
            .select_related('agency')
            .prefetch_related('amenities', 'images')
        )
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset           = Booking.objects.select_related('property')
    serializer_class   = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        data    = request.data
        prop_id = data.get('property') or data.get('property_id')

        if not prop_id:
            return Response(
                {'error': 'Property ID is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            prop = Property.objects.get(id=prop_id)
        except Property.DoesNotExist:
            return Response(
                {'error': 'Property not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        booking = Booking.objects.create(
            property=prop,
            customer_name=data.get('customer_name', ''),
            customer_phone=data.get('customer_phone', ''),
            date=data.get('date'),
            time=data.get('time'),
        )

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED,
        )
class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset           = Amenity.objects.all()
    serializer_class   = AmenitySerializer
    permission_classes = [AllowAny] 