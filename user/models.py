from django.db import models

class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'userProfiles'

    def __str__(self):
        return self.username
    
    @property
    def is_authenticated(self):
        return True

class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)

    class Meta:
        db_table = 'userPosts'

    def __str__(self):
        return self.title
