from django.test import TestCase
from .models import Profile

class ProfileModelTest(TestCase):

    def setUp(self):
        """
        Set up test data for the Profile model.
        """
        # Create parents
        self.father = Profile.objects.create(first_name="John", last_name="Doe")
        self.mother = Profile.objects.create(first_name="Jane", last_name="Doe")

        # Create siblings (full siblings: same father and mother)
        self.child1 = Profile.objects.create(first_name="Alice", last_name="Doe", father=self.father, mother=self.mother)
        self.child2 = Profile.objects.create(first_name="Bob", last_name="Doe", father=self.father, mother=self.mother)
        self.child3 = Profile.objects.create(first_name="Charlie", last_name="Doe", father=self.father, mother=self.mother)

        # Create a half-sibling (same father, different mother)
        self.half_sibling = Profile.objects.create(first_name="Daisy", last_name="Doe", father=self.father)

        # Create another unrelated profile
        self.unrelated = Profile.objects.create(first_name="Eve", last_name="Smith")

    def test_get_full_siblings(self):
        """
        Test that get_full_siblings correctly identifies full siblings.
        """
        # Test for child1
        full_siblings = self.child1.get_full_siblings()
        self.assertIn(self.child2, full_siblings)
        self.assertIn(self.child3, full_siblings)
        self.assertNotIn(self.child1, full_siblings)  # Exclude self
        self.assertNotIn(self.half_sibling, full_siblings)
        self.assertNotIn(self.unrelated, full_siblings)

        # Test for child2
        full_siblings = self.child2.get_full_siblings()
        self.assertIn(self.child1, full_siblings)
        self.assertIn(self.child3, full_siblings)

    def test_no_full_siblings(self):
        """
        Test profiles with no full siblings.
        """
        full_siblings = self.half_sibling.get_full_siblings()
        self.assertEqual(full_siblings.count(), 0)

        full_siblings = self.unrelated.get_full_siblings()
        self.assertEqual(full_siblings.count(), 0)
