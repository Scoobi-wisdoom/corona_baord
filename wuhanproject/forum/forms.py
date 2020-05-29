from django import forms
from forum.models import Post, Comment


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']

    def save(self, commit=True):
        blog_post = self.instance
        blog_post.title = self.cleaned_data['title']
        blog_post.body = self.cleaned_data['body']

        if commit:
            blog_post.save()
        return blog_post


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(attrs={
        'class': 'form-control content',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '3',
    }))
    class Meta:
        model = Comment
        fields = ['content']

