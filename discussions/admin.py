from django.contrib import admin
from .models import Discussion, Reply, ReplyVote

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'author', 'pinned', 'created_at']
    list_filter = ['pinned', 'created_at', 'course']
    search_fields = ['title', 'content', 'author__username']
    raw_id_fields = ['course', 'author']
    list_editable = ['pinned']
    date_hierarchy = 'created_at'

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['discussion', 'author', 'created_at', 'upvote_count']
    list_filter = ['created_at', 'discussion__course']
    search_fields = ['content', 'author__username', 'discussion__title']
    raw_id_fields = ['discussion', 'author']

@admin.register(ReplyVote)
class ReplyVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'reply', 'is_upvote', 'created_at']
    list_filter = ['is_upvote', 'created_at']
    search_fields = ['user__username', 'reply__content']
    raw_id_fields = ['user', 'reply']