from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views


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


# checa se os caminhos das URLs estão apontando para as views corretas.
class RecipeViewsTest(TestCase):  
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(
            reverse("recipes:home")
        )
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse("recipes:category", kwargs={"category_id": 1})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse("recipes:recipe", kwargs={"id": 1})
        )
        self.assertIs(view.func, views.recipe)
