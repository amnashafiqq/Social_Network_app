from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import Post,User


class PostAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_post(self):
        # Create a user and authenticate
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        # Send a POST request to create a post
        data = {'content': 'Test post'}
        response = self.client.post('/posts/create/', data)

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Post created successfully')

        # Optionally, you can check if the post is created in the database
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.content, 'Test post')
        self.assertEqual(post.user, user)
