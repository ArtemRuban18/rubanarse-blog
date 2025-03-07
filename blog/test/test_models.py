from django.test import TestCase
from blog.models import Category,Post, Comment
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            title="Category 1",
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Category 1")

    def test_object_creation(self):
        self.assertEqual(Category.objects.count(), 1)

    def test_category_isinstance(self):
        self.assertIsInstance(self.category, Category)
    
    def test_category_count(self):
        self.assertEqual(Category.objects.count(), 1)
    
    def test_auto_slug_category(self):
        self.assertTrue(self.category.slug)

class PostModelTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username = 'testuser', password = 'testpassword')
        self.category = Category.objects.create(title = 'Test category')
        self.category2 = Category.objects.create(title = 'Category 2')
        self.post = Post.objects.create(
            title = "test title",
            content = "test content",
            category = self.category,
            author = self.author,
            status = 'published',
        )

    def test_post_creation(self):
        self.assertTrue(self.post.title)
        self.assertTrue(self.post.content)
        self.assertTrue(self.post.category)
        self.assertTrue(self.post.author)
        self.assertTrue(self.post.status)
        self.assertTrue(self.post.created_at)
        self.assertTrue(self.post.updated_at)

        self.assertEqual(self.post.title, 'test title')
        self.assertEqual(self.post.content, 'test content')
        self.assertEqual(self.post.views, 0)
        self.assertEqual(Post.objects.count(),1)
        self.assertEqual(str(self.post), 'test title')
        self.assertIsInstance(self.post, Post)
    
    def test_post_str(self):
        self.assertEqual(str(self.post.title), self.post.title)
    
    def test_post_category_relation(self):
        self.assertEqual(self.post.category,self.category)
    
    def test_post_author_relation(self):
        self.assertEqual(self.post.author, self.author)
    
    def test_auto_slug_post(self):
        self.assertTrue(self.post.slug)
    
    def test_change_category_in_post(self):
        self.post.category = self.category2
        self.post.save()
        self.assertEqual(self.post.category, self.category2)

    def test_negative_views_count(self):
        self.post.views = -10

        with self.assertRaises(ValidationError):
            self.post.full_clean()

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = self.author = User.objects.create_user(username = 'testuser', password = 'testpassword')
        self.category = Category.objects.create(title = 'Test category')
        self.post = Post.objects.create(
            title = "test title",
            content = "test content",
            category = self.category,
            author = self.author,
            status = 'published',
        )
        self.comment = Comment.objects.create(user = self.user, post = self.post, comment = 'anything comment')

    def test_comment_creation(self):
        self.assertTrue(self.comment.user)
        self.assertTrue(self.comment.post)
        self.assertTrue(self.comment.comment)
        self.assertTrue(self.comment.created_at)
        self.assertEqual(self.comment.comment, 'anything comment')
    
    def test_comment_str(self):
        self.assertEqual(str(self.comment), f"{self.user} commited {self.post.title}")

    def test_comment_user_relation(self):
        self.assertEqual(self.comment.user, self.user)

    def test_comment_post_relation(self):
        self.assertEqual(self.comment.post, self.post)
