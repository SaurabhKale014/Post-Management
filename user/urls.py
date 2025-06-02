from django.urls import path
from .views import RegisterView, LoginView, CreatePostView , ListPostsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
    path('posts/', ListPostsView.as_view(), name='list_posts_all'),
    path('posts/<int:post_id>/', ListPostsView.as_view(), name='list_posts'),
]
