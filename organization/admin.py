from django.contrib import admin

from .models import UserBase


# Register your models here.
@admin.register(UserBase)
class UserBaseAdmin(admin.ModelAdmin):
    actions = ["export_username"]

    def get_list_display(self, request):
        fields = [field.name for field in self.model._meta.fields]
        fields.remove("password")
        return fields
