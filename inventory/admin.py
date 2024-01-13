from django.contrib import admin

from .models import *

# Register your models here.
model_classes = [cls for name, cls in vars().items() if isinstance(cls, type) and issubclass(cls, models.Model)]

for model in model_classes:
    admin.site.register(model)