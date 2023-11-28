from django.db import models

def grabValue(d : dict):
    return list(d.values())[0]

# auto generated products 
class Product(models.Model):
    name = models.CharField(max_length=128)
    vendor = models.CharField(max_length=128)
    red = models.SmallIntegerField()
    green = models.SmallIntegerField()
    blue = models.SmallIntegerField()
    url = models.CharField(max_length=2048)
    brand = models.CharField(max_length=256, blank=True, null=True)
    colorcode = models.CharField(max_length=128, blank=True, null=True)
    price = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'products'
    
    @staticmethod
    def getBrands():
        '''
        Returns the full list of brands in the database alphabetically
        '''
        return [""] + list(map(grabValue, list(Product.objects.values('brand').distinct().order_by('brand'))))