import os

from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

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
        ctx.update(
            {'recipes': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


class CategoryListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = None
    ordering = ['-id']
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        category_id = self.kwargs.get('category_id')
        filtered_qs = qs.filter(
            category__id=category_id,
            is_published=True,
        )
        return filtered_qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        recipes_list = self.object_list
        if recipes_list:
            category_name = recipes_list.first().category.name
            ctx['title'] = f'{category_name} - Category | '

        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
            }
        )
        return ctx


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by("-id")
    )

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        "recipes": page_obj,
        "pagination_range": pagination_range,
        "title": f"{recipes[0].category.name} - Category | "
    }

    return render(request, "recipes/pages/category.html", context)


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


def search(request):
    messages.success(request, 'Epa, você foi pesquisar algo que eu vi.')

    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    context = {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&={search_term}',
    }

    return render(request, 'recipes/pages/search.html', context)
