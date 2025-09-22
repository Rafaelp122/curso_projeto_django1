import os

from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        filtered_qs = qs.filter(
            is_published=True,
        )
        return filtered_qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update({
            'recipes': page_obj,
            'pagination_range': pagination_range,
        })
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        filtered_qs = qs.filter(
            category__id=self.kwargs.get('category_id'),
        )
        return filtered_qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        recipes_list = self.object_list
        if recipes_list:
            category_name = recipes_list.first().category.name
            ctx['title'] = f'{category_name} - Category | '

        return ctx


def recipe(request, id):
    recipe = get_object_or_404(
        Recipe,
        pk=id,
        is_published=True,
    )

    context = {
        "recipe": recipe,
        "is_detail_page": True,
    }

    return render(request, "recipes/pages/recipe-view.html", context)


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        qs = super().get_queryset(*args, **kwargs)

        filtered_qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
        )
        return filtered_qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        search_term = self.request.GET.get('q', '').strip()

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&={search_term}',
        })

        return ctx
