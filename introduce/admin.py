from django.contrib import admin

from introduce.models import Apply, DriverApply, Level


@admin.register(Apply)

class ApplyAdmin(admin.ModelAdmin):
    pass

@admin.register(DriverApply)

class DriverAdmin(admin.ModelAdmin):
    pass

@admin.register(Level)

class LevelAdmin(admin.ModelAdmin):
    pass
