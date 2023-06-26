from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import Post, User


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

    def test_get_post(self):
        # Create a user and a post
        user = User.objects.create_user(username='testuser', password='testpassword')
        post = Post.objects.create(content='Test post', user=user)

        # Send a GET request to retrieve the post
        response = self.client.get(f'/posts/{post.id}/')

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test post')
        self.assertEqual(response.data['user'], user.id)

    def test_update_post(self):
        # Create a user and a post
        user = User.objects.create_user(username='testuser', password='testpassword')
        post = Post.objects.create(content='Test post', user=user)

        # Authenticate as the post owner
        self.client.force_authenticate(user=user)

        # Send a PUT request to update the post
        data = {'content': 'Updated post'}
        response = self.client.put(f'/posts/{post.id}/', data)

        # Check the response status code and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated post')

        # Refresh the post from the database and check if it's updated
        post.refresh_from_db()
        self.assertEqual(post.content, 'Updated post')

    def test_delete_post(self):
        # Create a user and a post
        user = User.objects.create_user(username='testuser', password='testpassword')
        post = Post.objects.create(content='Test post', user=user)

        # Authenticate as the post owner
        self.client.force_authenticate(user=user)

        # Send a DELETE request to delete the post
        response = self.client.delete(f'/posts/{post.id}/')

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the post is deleted from the database
        self.assertFalse(Post.objects.filter(id=post.id).exists())
