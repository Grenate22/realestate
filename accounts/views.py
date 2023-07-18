from rest_framework import viewsets,permissions,status
from rest_framework.response import Response
from . models import UserAccount
from . serializers import SignupSerializer

class SignUpViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = UserAccount.objects.all()
    serializer_class = SignupSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        response_data = {"message":"Account created successfully.","user_id":"user.id","email":"user.email",}
        headers = self.get_success_headers(serializer.data)
        return Response(response_data,status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        return serializer.save()