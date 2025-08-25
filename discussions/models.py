from django.db import models
from users.models import User
from courses.models import Course

class Discussion(models.Model):
    """Course discussion forum"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='discussions')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pinned = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-pinned', '-created_at']
    
    def __str__(self):
        return self.title

class Reply(models.Model):
    """Replies to discussions"""
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, through='ReplyVote', related_name='upvoted_replies')
    
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Replies"
    
    def __str__(self):
        return f"Reply to {self.discussion.title}"
    
    @property
    def upvote_count(self):
        return self.votes.filter(is_upvote=True).count()

class ReplyVote(models.Model):
    """Voting system for replies"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='votes')
    is_upvote = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'reply']