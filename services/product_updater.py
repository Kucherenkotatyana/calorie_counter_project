from django.core.paginator import Paginator

from .nutrition import NutritionAPIClient, ProductNotFoundException, NutritionAPIException
from product.models import Product
from celery.utils.log import get_task_logger

logger = get_task_logger("celery_logger")


class ProductUpdater:

    def __init__(self, batch_size):
        self._model = Product
        self._batch_size = batch_size

    def update(self):
        products_queryset = self._model.objects.all().order_by('id')
        paginator = Paginator(products_queryset, self._batch_size)

        for page_number in paginator.page_range:
            page = paginator.page(page_number)

            product_names = [product.name for product in page.object_list]

            try:
                updated_products = self._get_actual_calories(product_names)
            except (ProductNotFoundException, NutritionAPIException):
                logger.info("products not found")
                continue

            self._update_model(page, updated_products)

    def _get_actual_calories(self, product_names):
        api_client = NutritionAPIClient()
        updated_products = api_client.get_multiple_products_calories(product_names)

        return updated_products

    def _update_model(self, page, updated_products):
        updates = []
        for obj in page.object_list:
            if obj.name in updated_products:
                if obj.calories != updated_products[obj.name]:
                    obj.calories = updated_products[obj.name]
                    updates.append(obj)

        self._model.objects.bulk_update(updates, ["calories"])
