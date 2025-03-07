from django.test import TestCase, Client
from blog.views import *
from django.urls import reverse
from blog.models import *

class IndexViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(title='Test Category')
        self.tag1 = Tag.objects.create(name = 'tag1')
        self.tag2 = Tag.objects.create(name = 'tag2')
        for i in range(25):
            post = Post.objects.create(
                title=f'Test Post {i}',
                category=self.category,
                content='This is a test content.',
                slug=f'test-post{i}',
                author=self.user,
                status='published' if i%2 == 0 else 'checkout'
            )

            post.tags.add(self.tag1 if i % 2 == 0 else self.tag2)
    
    def test_tempalte_use(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_status_code(self):
        url = reverse(index)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_view_index_context(self):
        response = self.client.get(self.url)

        self.assertIn('categories', response.context)
        self.assertIn('page_obj', response.context)
        self.assertIn('tags', response.context)
        self.assertIn('latest_posts', response.context)
        self.assertIn('status', response.context)
        self.assertIn('posts', response.context)

    def test_view_index_pagination(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['page_obj']), 10)

        response = self.client.get(self.url + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
    
    def test_tags_top(self):
        response = self.client.get(self.url)
        tags = list(Tag.objects.annotate(num_count=Count('taggit_taggeditem_items')))
        self.assertEqual(set(response.context['tags']), set(tags))
    
    def test_latest_post_in_view(self):
        response = self.client.get(self.url)
        posts = Post.objects.filter(status='published')
        latest_posts = list(posts.order_by('-created_at')[:3])
        self.assertEqual(list(response.context['latest_posts']), latest_posts)

class DetailPostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(title='Test Category')
        self.tag = Tag.objects.create(name='tag1')
        self.post = Post.objects.create(
            title='Test Post',
            category=self.category,
            content='This is a test content.',
            slug='test-post',
            author=self.user,
            status='published',
            views=0
        )
        self.post.tags.add(self.tag)

        self.url = reverse('detail_post', kwargs={'slug': self.post.slug})

    def test_redirect_not_logged_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_status_code(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200) 
    
    def test_add_view_increment(self):
        self.client.login(username='testuser', password='testpassword')
        initial_view = self.post.views
        self.client.get(self.url)
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, initial_view + 1)
    
    def test_comment_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.comment = Comment.objects.create(
            user = self.user,
            post = self.post,
            comment = "something"
        )
        self.assertIn('comments', response.context)
        self.assertEqual(len(response.context['comments']), 1)

    def test_view_detail_post_context(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('post', response.context)
        self.assertIn('comments', response.context)
        self.assertIn('latest_posts', response.context)
        self.assertIn('comment_form', response.context)

    def test_template_use(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'detail_post.html')

class PostByCategoryTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category1 = Category.objects.create(title='Test Category', slug='test-category')
        self.category2 = Category.objects.create(title='Test Category 2', slug='test-category-2')
        self.tag1 = Tag.objects.create(name='tag1')

        for i in range(25):
            post = Post.objects.create(
                title=f'Test Post {i}',
                category=self.category1 if i % 2 == 0 else self.category2,
                content='This is a test content.',
                slug=f'test-post-{i}',
                author=self.user,
                status='published'
            )
            post.tags.add(self.tag1)
        self.url = reverse('post_by_category', kwargs={'slug': self.category1.slug})
        self.url_category1 = reverse('post_by_category', kwargs={'slug': self.category1.slug})
        self.url_category2 = reverse('post_by_category', kwargs={'slug': self.category2.slug})

    def test_template_use(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'post_by_category.html')

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_pagination(self):
        response = self.client.get(self.url_category1)
        self.assertEqual(len(response.context['page_obj']), 9)

        response = self.client.get(self.url_category1 + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

        response = self.client.get(self.url_category2)
        self.assertEqual(len(response.context['page_obj']), 9)
        response = self.client.get(self.url_category2 + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
    
    def test_post_by_category_context(self):
        response = self.client.get(self.url)
        self.assertIn('posts', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('page_obj', response.context)
        self.assertIn('latest_posts', response.context)
        self.assertIn('tags', response.context)


class PostByAuthorTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.tag1 = Tag.objects.create(name='tag1')

        for i in range(25):
            post = Post.objects.create(
                title=f'Test Post {i}',
                category=self.category,
                content='This is a test content.',
                slug=f'test-post-{i}',
                author=self.user if i % 2 == 0 else self.user2,
                status='published'
            )
            post.tags.add(self.tag1)
        self.url = reverse('post_by_author', kwargs={'username': self.user.username})
        self.url_author1 = reverse('post_by_author', kwargs={'username': self.user.username})
        self.url_author2 = reverse('post_by_author', kwargs={'username': self.user2.username})

    def test_template_use(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'post_by_author.html')

    def test_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_pagination(self):
        response = self.client.get(self.url_author1)
        self.assertEqual(len(response.context['page_obj']), 9)

        response = self.client.get(self.url_author1 + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

        response = self.client.get(self.url_author2)
        self.assertEqual(len(response.context['page_obj']), 9)
        response = self.client.get(self.url_author2 + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
    
    def test_post_by_category_context(self):
        response = self.client.get(self.url)
        self.assertIn('posts', response.context)
        self.assertIn('author', response.context)
        self.assertIn('page_obj', response.context)
        self.assertIn('latest_posts', response.context)
        self.assertIn('tags', response.context)
class PostByTagTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.tag = Tag.objects.create(name='tag')
        self.tag1 = Tag.objects.create(name='tag1')
        self.tag2 = Tag.objects.create(name='tag2')

        for i in range(25):
            post = Post.objects.create(
                title=f'Test Post {i}',
                category=self.category,
                content='This is a test content.',
                slug=f'test-post-{i}',
                author=self.user,
                status='published',
            )

            post.tags.add(self.tag1 if i % 2 == 0 else self.tag2)

        self.url_tag1 = reverse('post_by_tag', kwargs={'name': self.tag1.name})
        self.url_tag2 = reverse('post_by_tag', kwargs={'name': self.tag2.name})

    def test_template_use_tag1(self):
        response = self.client.get(self.url_tag1)
        self.assertTemplateUsed(response, 'post_by_tag.html')

    def test_status_code_tag1(self):
        response = self.client.get(self.url_tag1)
        self.assertEqual(response.status_code, 200)

    def test_template_use_tag2(self):
        response = self.client.get(self.url_tag2)
        self.assertTemplateUsed(response, 'post_by_tag.html')

    def test_status_code_tag2(self):
        response = self.client.get(self.url_tag2)
        self.assertEqual(response.status_code, 200)

    def test_view_pagination(self):
        response = self.client.get(self.url_tag1)
        self.assertEqual(len(response.context['page_obj']), 9)

        response = self.client.get(self.url_tag1 + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

        response = self.client.get(self.url_tag2)
        self.assertEqual(len(response.context['page_obj']), 9)
        response = self.client.get(self.url_tag2 + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
    
    def test_post_by_category_context(self):
        response = self.client.get(self.url_tag1)
        self.assertIn('posts', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('page_obj', response.context)
        self.assertIn('latest_posts', response.context)
        self.assertIn('tag', response.context)
        self.assertIn('tags', response.context)
