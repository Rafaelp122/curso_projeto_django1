from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.core.paginator import Paginator

from utils.pagination import make_pagination_range
from recipes.models import Recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by("-id")

    try:
        current_page = request.GET.get('page', 1)
    except ValueError:
        current_page = 1

    paginator = Paginator(recipes, 9)
    page_obj = paginator.get_page(1)

    pagination_range = make_pagination_range(
        paginator.page_range,
        4,
        current_page,
    )

    context = {
        "recipes": page_obj,
        'pages': pagination_range,
        }

    return render(request, "recipes/pages/home.html", context)


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by("-id")
    )

    context = {
        "recipes": recipes,
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

    context = {
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': recipes,
    }

    return render(request, 'recipes/pages/search.html', context)
