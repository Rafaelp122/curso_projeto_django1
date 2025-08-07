from django.test import TestCase
from django.urls import reverse


# checa se os nomes das URLs geram os caminhos corretos.
class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        url = reverse("recipes:home")
        self.assertEqual(url, "/")

    def test_recipe_category_url_is_correct(self):
        url = reverse("recipes:category", kwargs={"category_id": 1})
        self.assertEqual(url, "/recipes/category/1/")

    def test_recipe_detail_url_is_correct(self):
        url = reverse("recipes:recipe", kwargs={"id": 1})
        self.assertEqual(url, "/recipes/1/")

    def test_recipe_search_url_is_correct(self):
        url = reverse("recipes:search")
        self.assertEqual(url, "/recipes/search/")
