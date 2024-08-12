from django.db import models

# Create your models here.
class Inventory(models.Model):
    name= models.CharField(max_length=50)
    cost_per_item= models.DecimalField(max_digits=19,decimal_places=2,null=False)
    quantity_in_stock= models.IntegerField(max_length=10, null=False)
    quantity_sold= models.IntegerField(max_length=10, null=False)
    sales= models.DecimalField(max_digits=19, decimal_places=2, null= False)

    stock_date= models.DateField(auto_now=True)
    last_sales_date= models.DateField(auto_now=True)

    def __str__(self):
        return self.name  