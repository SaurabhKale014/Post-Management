from rest_framework import serializers
from .models import UserProfile, Post
from django.contrib.auth.hashers import make_password, check_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = UserProfile.objects.get(email=data['email'])
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("User with this email not found")

        if not check_password(data['password'], user.password):
            raise serializers.ValidationError("Incorrect password")

        data['user'] = user
        return data

class PostSerializer(serializers.ModelSerializer):
    Post_id=serializers.IntegerField(source='id',read_only=True)
    class Meta:
        model = Post
        fields = ['Post_id','title', 'content', 'image']
    
     
