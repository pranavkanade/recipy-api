from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags api"""

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            'test1@mail.com',
            'test1pass'
        )

        self.user2 = get_user_model().objects.create_user(
            'test2@mail.com',
            'test2pass'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user1)


    def test_retrieve_tags(self):
        """Test retrieving the tags list"""
        Tag.objects.create(user=self.user1, name="vegan")
        Tag.objects.create(user=self.user1, name="dessert")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test, each user has individual list"""
        Tag.objects.create(user=self.user2, name="fruity")
        tag = Tag.objects.create(user=self.user1, name="spicy")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_success(self):
        """Test creating a new tag"""
        payload= {
            'name': 'test tag'
        }
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.all().filter(
            user=self.user1,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating invalid tag"""
        payload = {'name': ""}
        res = self.client.post(payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

