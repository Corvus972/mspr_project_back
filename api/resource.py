from import_export import resources
from api.models import *


class ProductResource(resources.ModelResource):
    """
    Product Resource for Import Export Library
    """

    class Meta:
        model = Product
