from django.urls import reverse
from blog.forms import CreatePostForm, CommentForm
from django.test import TestCase, Client
from blog.models import Post, Comment, Category
from django.contrib.auth.models import User

class CreatePostFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_post')
        self.user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)
        self.client.login(username='testuser', password='testpassword')

        self.category = Category.objects.create(title='Test Category')

        self.data = {
            'title': 'Test Post',
            'content': 'Test content',
            'category': self.category.id,
            'tags': 'tag1, tag2',
            'author': self.user.id,
        }

    def test_create_post_form(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.first()
        self.assertEqual(post.title, self.data['title'])
        self.assertEqual(post.content, self.data['content'])
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.tags.count(), 2)

    def test_create_post_form_invalid(self):
        form_data = {'title': '', 'content': '', 'category': '', 'tags': ''}
        form = CreatePostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_for_not_staff_user(self):
        self.user.is_staff = False
        self.user.save()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 0)

class CreateCommentFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.category = Category.objects.create(title='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            category=self.category,
            author=self.user,
            status='published',
            views=0
        )

        self.url = reverse('detail_post', kwargs={'slug': self.post.slug})

        self.data = {'comment': 'some comment'}

    def test_create_comment_form(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.first()
        self.assertEqual(comment.comment, self.data['comment'])
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)

    def test_invalid_comment_form(self):
        data = {'comment': ''}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('comment', form.errors)

    def test_for_not_logged_user(self):
        self.client.logout()
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)
