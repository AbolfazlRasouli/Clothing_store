from .models import Category


def subcategory(request):

    categories = Category.objects.all()
    return {'category': categories}
