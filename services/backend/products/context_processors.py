from .models import Category

def menu_categories(request):
    """Передает список разделов во все шаблоны сайта"""
    return {
        'menu_categories': Category.objects.all()
    }