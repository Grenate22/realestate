from django.shortcuts import render
from rest_framework import permissions,viewsets,status
from .models import Contact
from .serializers import ContactSerializer
from django.core.mail import send_mail
from rest_framework.response import Response

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        try:
            self.send_email(serializer.validated_data)
        except Exception as e:
            return Response(
                {'error': 'An error occurred while sending the email.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {'success': 'Message sent successfully'},
            status=status.HTTP_201_CREATED
        )
    
    def perform_create(self, serializer):
        serializer.save()

    def send_email(self,data):
        send_mail(
                'New Contact Message',
                f"Name: {data['name']}\nEmail: {data['email']}\nMessage: {data['message']}",
                'karenfurst6@outlook.com',
                ['karenfurst6@gmail.com'],
                fail_silently=False,
            )