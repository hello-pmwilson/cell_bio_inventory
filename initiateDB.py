print("start success")

from inventory.models import *
# print(unit.objects.all())
# from django.db import IntegrityError

# #Load the initial defaults into pk 1 for applicable databases

# #First, set these desired values
# DEFAULT_UNIT = "unit(s)"
# DEFAULT_LAB = "lab"
# DEFAULT_LOCATION = "lab"
# DEFAULT_STATUS = "in the void"
# DEFAULT_CATEGORY = "lab stuff"
# DEFAULT_ITEM = "thing(s)"
# DEFAULT_VENDOR = "probably some monopoly"

# default_unit = unit(unit="unit(s)", unit_category="count")
# try:
#   default_unit.save()
# except IntegrityError:
#   print("Unit already exists.")

# item_query, created = item.objects.get_or_create(item=selected_item, defaults={'item_description':'TBD', 'category': category.objects.get(pk=1)})