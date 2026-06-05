from django.contrib import admin
from django.forms import ModelForm

from commercialoperator.components.main.models import FileExtensionWhitelist

@admin.register(FileExtensionWhitelist)
class FileExtensionWhitelistAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "model",
    )
    list_display = (
        "name",
        "model",
    )
    form = ModelForm