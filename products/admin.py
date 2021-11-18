from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductBOM)
admin.site.register(ProductGroup)
admin.site.register(ProductSubGroup)
admin.site.register(Material)
admin.site.register(MaterialGroup)
admin.site.register(MaterialOrder)
admin.site.register(Supplier)
admin.site.register(SupplierMaterial)
admin.site.register(BOMItem)
