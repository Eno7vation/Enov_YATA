from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.contrib.admin.filters import FieldListFilter
from tech.models import Post, Activity, Category, Profile, Tag, Bug
from config.utils.csv_export import ExportCsvMixin

class MultiSelectFieldListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = field_path + '__in'
        self.lookup_val = request.GET.get(self.lookup_kwarg, [])
        self.field = field
        super().__init__(field, request, params, model, model_admin, field_path)

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, changelist):
        choices = list(self.field.choices)
        selected_choices = set(self.lookup_val)
        for choice in choices:
            if choice[0] in selected_choices:
                choice = choice[0], choice[1], True
            yield choice



@admin.register(Post)
class PostAdmin(SummernoteModelAdmin, ExportCsvMixin):
    list_display = ['id', 'author']
    list_display_links = ['id']
    search_fields = ['caption']
    summernote_fields = ['caption']
    actions = ["export_as_csv"]

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    actions = ["export_as_csv"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_filter = (('status', MultiSelectFieldListFilter),)
    search_fields = ['description']
    ordering = ('status',)

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            if obj.status in ['Solve', 'Impossible']:
                obj.bug_rock = max(obj.bug_rock - 1, 0)
        obj.save()

    actions = ["export_as_csv"]
