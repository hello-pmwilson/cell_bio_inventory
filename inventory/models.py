from django.db import models

class unit(models.Model):
    unit = models.CharField(max_length=10, default="unit(s)", unique=True)
    unit_category = models.CharField(max_length=10, default="count")

    def __str__(self):
        return self.unit
# options for units to choose from

class location(models.Model):
    lab = models.CharField(max_length=25, default="lab")
    location = models.CharField(max_length=50, default="lab")

    class Meta:
        unique_together = ('lab', 'location')

    def __str__(self):
        return f"{self.lab} {self.location}"  
# options for locations to choose from

class status(models.Model):
    status = models.CharField(max_length=10, default="in the void", unique=True)

    def __str__(self):
        return self.status
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
# when requesting or ordering or etc items 
# current status indicates what stage the order/request/etc is in

class category(models.Model):
    category = models.CharField(max_length=20, default="lab stuff", unique=True)

    def __str__(self):
        return self.category
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
# when creating an item
# category references what type of thing the item is, for later filtering

class item(models.Model):
    item = models.CharField(max_length=100, default="thing(s)", unique=True)
    item_description = models.TextField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)

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
    amount = models.PositiveSmallIntegerField(default="1")
    unit = models.ForeignKey(unit, on_delete=models.SET_DEFAULT, default=1)
    location = models.ForeignKey(location, on_delete=models.SET_DEFAULT, default=1)
    notes = models.TextField(null=True, blank=True, default=None) 

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
    unit = models.ForeignKey(unit, on_delete=models.SET_DEFAULT, default=1)
    

    class Meta:
        verbose_name = "Purchase Reference"
        verbose_name_plural = "Purchase References"
# items and their costs from different vendors
# for future reference when ordering or making budgets


class on_request(models.Model):
    item = models.ForeignKey(item, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
    unit = models.ForeignKey(unit, on_delete=models.SET_DEFAULT, default=1)
    status = models.ForeignKey(status, on_delete=models.SET_DEFAULT, default=1)

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"