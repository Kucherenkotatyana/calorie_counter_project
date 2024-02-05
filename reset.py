from product.models import Product


def reset():
    products = Product.objects.all()

    for product in products:
        product.calories = 10

    Product.objects.bulk_update(products, ['calories'])
