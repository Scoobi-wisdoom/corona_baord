from django.db import models
from django.conf import settings
from django.urls import reverse
from django import template

register = template.Library()


class Post(models.Model):
    title = models.CharField(max_length=80, null=False, blank=False)
    body = models.TextField(max_length=5000, blank=True, null=True)
    featured = models.BooleanField(default=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")  # 글을 수정하지 않으면 date_published와 동일
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accumulated_comment_count = models.IntegerField(default=0, blank=None, null=True)

    # featured                = models.BooleanField()                         # JustDjango
    # categories              = models.ManyToManyField(Category)              # 글의 카테고리를 객관식으로 지정 가능. admin이 설정을 해주어야 한다.

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # JustDjango
        return reverse('forum:detail', kwargs={
            'id': self.id,
            'title': self.title
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('date_updated')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count() + PostViewIP.objects.filter(post=self).count()

    @property
    def up_count(self):
        return PostUp.objects.filter(post=self).count()


class Comment(models.Model):
    content = models.TextField(max_length=5000, null=False, blank=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    comment_id = models.IntegerField(default=0, blank=None, null=True)

    def save(self, *args, **kwargs):
        new_accumulated_comment_count = self.post.accumulated_comment_count + 1
        self.post.accumulated_comment_count = new_accumulated_comment_count
        self.post.save()
        self.comment_id = new_accumulated_comment_count
        super(Comment, self).save(*args, **kwargs)

    def __str__(self):
        return self.author.username


class PostView(models.Model):  # JustDjango 조회수 체크
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # JustDjango
    post = models.ForeignKey('Post', related_name='post_views', on_delete=models.CASCADE)  # JustDjango

    def __str__(self):
        return self.user.username


class PostViewIP(models.Model):
    ip = models.CharField(max_length=100, null=False, blank=False)  # JustDjango
    post = models.ForeignKey('Post', related_name='post_view_ips', on_delete=models.CASCADE)  # JustDjango

    def __str__(self):
        return self.ip


class PostUp(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # JustDjango
    post = models.ForeignKey('Post', related_name='post_ups', on_delete=models.CASCADE)  # JustDjango

    def __str__(self):
        return self.user
