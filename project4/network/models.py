from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="current_author")
    time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} {self.author}, {self.content}, {self.time}"
    
class Following(models.Model):
    source = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_who_clicks")
    target = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_who_is_followed")

    class Meta:
        constraints = [
            # UnisqueConstraint means the combination of these two fields must be unique, no duplicates allowed
            models.UniqueConstraint(fields=["source", "target"], name="unique_follow_pair")
        ]

    def __str__(self):
        return f"{self.source} is following {self.target}."

class Like(models.Model):
    source = models.ForeignKey(User,on_delete=models.CASCADE, related_name="user_who_liked")
    target = models.ForeignKey(Post,on_delete=models.CASCADE, related_name="post_to_like")

    def __str__(self):
        return f"{self.id} {self.source} liked {self.target}"

