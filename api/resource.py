from import_export import resources
from api.models import *


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
