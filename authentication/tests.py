from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import Post, User

class PostAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_post(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)
       
        data = {'content': 'Test post', 'user': user.id}
        response = self.client.post('/posts/create/', data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.content, 'Test post')
        self.assertEqual(post.user, user)

    def test_like_post(self):     
        user = User.objects.create_user(username='testuser', password='testpassword')
        post = Post.objects.create(content='Test post', user=user)
        self.client.force_authenticate(user=user)
        response = self.client.post(f'/posts/{post.id}/like')
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

