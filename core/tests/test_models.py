from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@asdf.com", password="testpass"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModesTest(TestCase):

    def test_user_creation_with_email_is_successful(self):
        """
        Check if the user with the given email id and password is created successfully
        """
        email = "test@example.com"
        password = "pass1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalization(self):
        """
        Check if the user email provided converted to lower case
        """
        email = "test@EXAMPLE.com"
        password = "pass1324"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_email_format(self):
        """Do not let None val for email pass through"""
        with self.assertRaises(ValueError):
           email = None
           password = "asdf"
           user = get_user_model().objects.create_user(
               email=email,
               password=password
           )

    def test_super_user_creation(self):
        """
        Check if one can create super user
        """
        user = get_user_model().objects.create_superuser(
            email="test@eg.com",
            password="asdf"
        )

        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )

        self.assertEqual(str(tag), tag.name)


    def test_ingredients_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
