from django.db import models


# Create your models here.
class ProductGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductSubGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)


    def __str__(self):
        info = str(self.product_group) + ' > ' + str(self.name)
        return str(info)


class Product(models.Model):
    product_subgroup = models.ForeignKey(ProductSubGroup, on_delete=models.CASCADE)
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=100)
    unit_of_measure = models.CharField(max_length=10)
    weight = models.DecimalField(max_digits=5, decimal_places=3)
    weight_text = models.CharField(max_length=10)

    def __str__(self):
        product_info = str(self.code) + ' - ' + str(self.name)
        return str(product_info)


class MaterialGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    material_group = models.ForeignKey(MaterialGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    material = models.ManyToManyField(Material)

    def __str__(self):
        return self.name


class SupplierMaterial(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)


class MaterialOrder(models.Model):
    item = models.ForeignKey(SupplierMaterial, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)


class ProductBOM(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)


class BOMItem(models.Model):
    bom_id = models.ForeignKey(ProductBOM, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
