from rest_framework import serializers
import re
from .models import UserAccount

class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ('email','username','name','password1','password2')

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError("password do not match")
        
        if password1 and len(password1) < 6 :
            raise serializers.ValidationError("Password must be at least 6 character long")
        
        if password1 and not re.search(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%^&+=]).+$', password1):
            raise serializers.ValidationError("Password must contain at least one letter, one digit, and one special character.")
        

        return attrs

    def create(self, validated_data):
        password= validated_data.pop('password1')
        validated_data.pop('password2', None)
        user = UserAccount(**validated_data)
        user.set_password(password)
        user.save()
        return user