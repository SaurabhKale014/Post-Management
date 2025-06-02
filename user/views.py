from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post
from .serializers import RegisterSerializer, LoginSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

# Custom JWT Auth for manually-managed UserProfile
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserProfile

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user_id = validated_token["user_id"]
        try:
            return UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            raise AuthenticationFailed("User not found")

class CreatePostView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Post created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListPostsView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id=None):
        if post_id:
            post = get_object_or_404(Post, id=post_id, user=request.user)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=200)
        else:
            posts = Post.objects.filter(user=request.user)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=200)
    
    def put(self, request, post_id=None):
        if not post_id:
            return Response({"detail": "Post ID is required for update."}, status=400)

        post = get_object_or_404(Post, id=post_id, user=request.user)
        serializer = PostSerializer(post, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, post_id=None):
        if not post_id:
            return Response({"detail": "Post ID is required for deletion."}, status=400)

        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.delete()
        return Response({"detail": "Post deleted successfully"}, status=204)

    
