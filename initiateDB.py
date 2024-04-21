#run once when first deploying the site
#for intial DB set up, set the defaults first so they are pk=1
#run in the railway cli, personally I use wsl
#run railway link and select the desired db
#navigate to desired folder
#railway run python3 manage.py shell < initiateDB.py
from inventory.models import *
from django.db import IntegrityError

#set these desired default values
DEFAULT_UNIT = "unit(s)"
DEFAULT_UNIT_CATEGORY = "count"
DEFAULT_LAB = "lab"
DEFAULT_LOCATION = "lab"
DEFAULT_STATUS = "in the void"
DEFAULT_CATEGORY = "lab stuff"
DEFAULT_ITEM = "thing(s)"
DEFAULT_ITEM_DESCRIPTION = "for doing science and stuff"
DEFAULT_VENDOR = "probably some monopoly"
#Other Presets
STATUSES = ['on order', 'on request', 'waiting approval', 'approved', 'denied']
CATEGORIES = ['glassware', 'consumable', 'media']


#Units
default_unit = unit(unit=DEFAULT_UNIT, unit_category=DEFAULT_UNIT_CATEGORY)
try:
  default_unit.save()
  print("Default unit added.")
except IntegrityError:
  print("Default unit already exists.")

#Lab
default_lab = location(lab=DEFAULT_LAB, location=DEFAULT_LOCATION)
try:
  default_lab.save()
  print("Default lab added.")
except IntegrityError:
  print("Default lab location already exists.")

#Status
default_status = status(status="in the void")
try:
  default_status.save()
  print("Default status added")
except IntegrityError:
  print("Default status already exists.")

for stat in STATUSES:
  new_stat = status(status=stat)
  try:
    new_stat.save()
    print("New status added.")
  except IntegrityError:
    print("Status already exists.")

#Category
default_category = category(category=DEFAULT_CATEGORY)
try:
  default_category.save()
  print("Default category added.")
except IntegrityError:
  print("Default category already exists.")

for cat in CATEGORIES:
  new_cat = category(category=cat)
  try:
    new_cat.save()
    print("New category added.")
  except IntegrityError:
    print("Category already exists.")

#Item
default_item = item(item=DEFAULT_ITEM, item_description = DEFAULT_ITEM_DESCRIPTION, category=category.objects.get(category=DEFAULT_CATEGORY))
try:
  default_item.save()
  print("Default item added.")
except IntegrityError:
  print("Default item already exists.")

#Vendor
default_vendor = vendor(vendor=DEFAULT_VENDOR)
try:
  default_vendor.save()
  print("Default vendor added.")
except IntegrityError:
  print("Default vendor already exists.")