from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from .models import Realtor
from .serializers import RealtorSerializer

class RealtorViewSet(viewsets.ModelViewSet):
    permission_classes = permissions.AllowAny
    queryset = Realtor.objects.all()
    serializer_class = RealtorSerializer
    #allow only get requests for listing and retriving 
    http_method_names = ['get']
    pagination_class = None

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes ]
    
    @action(detail=False, methods=['get'])
    def top_sellers(self, request):
        top_sellers = Realtor.objects.filter(top_seller = True)
        serializer = self.get_serializer(top_sellers, many=True)
        return Response(serializer.data)

    