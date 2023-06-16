from django.contrib import admin
from accounts.models import Users
from config.utils.csv_export import ExportCsvMixin


@admin.register(Users)
class UserAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['name', 'username', 'nickname',
                    'car', 'post_num', 'post_limit',
                    'car_num', 'major']
    actions = ["export_as_csv"]

