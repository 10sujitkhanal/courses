from category.models import Categories

def get_all_category(request):
    data = {
        'category':Categories.get_all_category(Categories)
    }
    return data