from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

class unit(models.Model):
    unit = models.CharField(primary_key=True, max_length=10, default="unit(s)")

    def __str__(self):
        return self.unit
# options for units to choose from

class location(models.Model):
    location = models.CharField(primary_key=True, max_length=50, default="lab")

    def __str__(self):
        return self.location  
# options for locations to choose from

class status(models.Model):
    status = models.CharField(max_length=10, default="in the void")

    def __str__(self):
        return self.status
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
# when requesting or ordering or etc items 
# current status indicates what stage the order/request/etc is in

class category(models.Model):
    category = models.CharField(max_length=20, default="lab stuff")

    def __str__(self):
        return self.category
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
# when creating an item
# category references what type of thing the item is, for later filtering

class item(models.Model):
    item = models.CharField(max_length=100, default="thing(s)")
    item_description = models.TextField()
    category = models.ForeignKey(category, on_delete=models.SET_DEFAULT, default="lab stuff")

    def __str__(self):
        return self.item
# for basic item categories
# like 25mL flask, 25pk petri dishes 
# which will then be put into other databases with qty, etc

class vendor(models.Model):
    vendor = models.CharField(max_length=50, default="probably some monopoly")
    
    def __str__(self):
        return self.vendor
# options for vendors to choose from    

class inventory(models.Model):
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
    unit = models.ForeignKey(unit, on_delete=models.SET_DEFAULT, default=19)
    location = models.ForeignKey(location, on_delete=models.SET_DEFAULT, default="lab")

    def __str__(self):
        return f"{self.item}"
    class Meta:
        verbose_name = "Inventory"
        verbose_name_plural = "Inventory"
# the actual inventory where items, qty, and location are stored

class purchase_reference(models.Model):
    purchase_reference = models.AutoField(primary_key=True)
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    vendor = models.ForeignKey(vendor, on_delete=models.CASCADE)
    catalog = models.CharField(max_length=25)
    price = models.PositiveSmallIntegerField()
    amount = models.PositiveSmallIntegerField()
    unit = models.ForeignKey(unit, on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = "Purchase Reference"
        verbose_name_plural = "Purchase References"
# items and their costs from different vendors
# for future reference when ordering or making budgets


class on_request(models.Model):
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
    unit = models.ForeignKey(unit, on_delete=models.SET_DEFAULT, default=19)
    status = models.ForeignKey(status, on_delete=models.SET_DEFAULT, default="in the void")

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"