from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post,UserProfile
from .authentication import CustomJWTAuthentication
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer, PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .permissions import IsOwner,IsEmployee

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            return Response({
                'message': 'User registered successfully',
                'id':user.id,
                'username':user.username    
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BA_REQUEST)
    
class DeleteUserView(APIView):
    authentication_classes=[CustomJWTAuthentication]
    permission_classes=[IsAuthenticated,IsOwner]
    def delete(self,request,user_id=None):
        if not user_id:
            return Response({"detail":"User ID is required for deletion."}, status=400)
        user=get_object_or_404(UserProfile,id=user_id)
        user.delete()
        return Response({"detail":"User deleted successfully"},status=204)


class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'userID': user.id,
                'email':user.email,
                'role':user.role,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
      

class CreatePostView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Post created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OwnerPostsView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]  # Both authentication and Owner check

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        # To show post count
        post_count=posts.count()
        response_data={
            'total_posts':post_count,
            'posts':serializer.data,
            'message':f'Successfully retrived {post_count} posts.'
        }
        return Response(response_data, status=200)

    def put(self , request , post_id=None):
        if not post_id :
            return Response({"detail":"Post ID is required for update."}, status=400)
        post=get_object_or_404(Post , id=post_id)
        serializer=PostSerializer(post , data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ListPostsView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated ,IsEmployee ]

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