from django.contrib import admin
from .models import TestModel

# Register your models here.

class TestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'field',)

admin.site.register(TestModel, TestAdmin)

