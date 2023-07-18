from django.shortcuts import render
from django.db.models import Count
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import permissions, viewsets,filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Listing
from .serializers import ListingSerializer, ListingDetailSerializer
from datetime import datetime, timezone, timedelta

class ListingView(viewsets.ModelViewSet):
    queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
    permission_classes = (permissions.AllowAny,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['sale_type', 'price', 'bedrooms', 'home_type', 'bathrooms', 'sqft', 'days_passed', 'has_photos']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ListingDetailSerializer
        return ListingSerializer
    
    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes ]
    
    @action(detail=True, methods=['post'], permission_classes= [permissions.IsAuthenticated], url_path='contact-realtor')
    def contact_realtor(self, request):
        queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
        realtor_email = queryset.realtor.email
        full_address = queryset.get_full_address()
        subject = f"I want to make inquiry about {full_address}"
        message = request.data.get('message')
        sender_email = request.user.email
        recipient_list = [realtor_email]
        send_mail(subject, message, send_mail, recipient_list, fail_silently=False)
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        queryset = Listing.objects.order_by('-list_date').filter(is_published=True)
        data = self.request.data
        sale_type = data['sale_type']
        #i__exact is a filter function that find the exact word with case insensitive
        queryset = queryset.filter(sale_type__iexact=sale_type)
        
        price_min = data['price_min']
        price_max = data['price_max']
        if price_min is not None and price_max is not None:
            price_min = price_min.replace(',', '').replace('$', '').replace('+', '')
            price_max = price_max.replace(',', '').replace('$', '').replace('+', '')
            queryset = queryset.filter(price__gte=price_min, price__lte=price_max)
        elif price_min is not None:
            price_min = price_min.replace(',', '').replace('$', '').replace('+', '')
            queryset = queryset.filter(price__gte=price_min)

        elif price_max is not None:
            price_max = price_max.replace(',', '').replace('$', '').replace('+', '')
            queryset = queryset.filter(price__lte=price_max)
        
        bedrooms = data['bedrooms']
        if bedrooms is not None:
            if bedrooms.lower() == 'any':
                pass

            elif bedrooms[-1] == '+':   #what this is doing is that once we pass badrooms number we check to make sure the last index is + like 2+, or 50+
                min_bedrooms = int(bedrooms[:-1]) 
                queryset = queryset.filter(bedrooms__gte=min_bedrooms)
            else:
                bedrooms = int(bedrooms)
                queryset = queryset.filter(bedrooms=bedrooms)
    
        home_type = data['home_type']
        queryset = queryset.filter(home_type__iexact=home_type)

        bathrooms = data['bathrooms']
        if bathrooms == "0+":
            bathrooms = 0.0
        elif bathrooms == "1+":
            bathrooms = 1.0
        elif bathrooms == "2+":
            bathrooms = 2.0
        elif bathrooms == "3+":
            bathrooms = 3.0
        elif bathrooms == "4+":
            bathrooms = 4.0
        elif bathrooms == "5+":
            bathrooms = 5.0
        
        queryset = queryset.filter(bathrooms__gte=bathrooms)

        sqft = data["sqft"]
        if sqft == "1000+":
            sqft = 1000
        elif sqft == "1200":
            sqft = 1200 
        elif sqft == "1500":
            sqft = 1500 
        elif sqft == "2000":
            sqft = 2000 
        elif sqft == "Any":
            sqft = 0 
        if sqft != 0:
            queryset= queryset.filter(sqft__gte=sqft)

        days_passed = data["days_listed"]
        if days_passed =="1 or less":
            days_passed = 1
        elif days_passed == "2 or less":
            days_passed = 2
        elif days_passed == "5 or less":
            days_passed = 5
        elif days_passed == "10 or less":
            days_passed = 10
        elif days_passed == "20 or less":
            days_passed = 20
        elif days_passed == "Any":
            days_passed = 0
        
        for query in queryset:
            num_days = (datetime.now(timezone.utc) - query.list_date).days

            if days_passed != 0:
                if num_days > days_passed:
                    slug = query.slug
                    queryset = queryset.exclude(slug__iexact=slug)

        
        has_photos = data["has_photos"]
        if has_photos is not None:
            if has_photos[-1] == "+":
                min_photos = int(has_photos[:-1])
                queryset = queryset.annotate(num_photos=Count('photos')).filter(num_photos__gte=min_photos)
            else:
                has_photos = int(has_photos)
                queryset = queryset.annotate(num_photos=Count('photos')).filter(num_photos=has_photos)
        
        open_house = data["open_house"]
        #for the openhouse api testing with postman use 1 or 0 for true or false
        queryset = queryset.filter(open_house__iexact=open_house)

        keywords = data["keywords"]
        queryset = queryset.filter(description__icontains=keywords)
        serializer = ListingSerializer(queryset, many=True)
        return Response(serializer.data)

    


         


        
        
        

        
    
        