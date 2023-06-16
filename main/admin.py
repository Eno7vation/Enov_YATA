from django.contrib import admin

from accounts.models import Suspension
from config.utils.csv_export import ExportCsvMixin
from main.models import user_reservation, Post, Road


@admin.register(Post)
class PostAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['car_user', 'date', 'time',
                    'money', 'car_num',
                    'address_kakao_start', 'address_kakao_end',
                    'start_detail', 'end_detail']
    actions = ["export_as_csv"]



@admin.register(user_reservation)
class User_reservationAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['user', 'address_kakao_start', 'address_kakao_end',
                    'start_detail', 'end_detail', 'reservation_date',
                    'remove']
    actions = ["export_as_csv"]


@admin.register(Road)
class RoadAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['user', 'road', 'road_num', 'road_check']
    actions = ["export_as_csv"]

@admin.register(Suspension)
class SuspensionAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]