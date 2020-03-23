from django.contrib import admin
from diagnosis.models import *
from import_export.admin import ImportExportModelAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from import_export import resources
from import_export.admin import ExportActionMixin
from django_admin_listfilter_dropdown.filters import DropdownFilter,ChoiceDropdownFilter


class diagnosisAdmin(ExportActionMixin, admin.ModelAdmin):
    date_hierarchy = 'date'
    list_display=('name','phone','email','city','state',)
    list_filter = (('state',ChoiceDropdownFilter),('profile',ChoiceDropdownFilter),('date',DateRangeFilter))
    search_fields=('name','phone','email','city')

# Register your models here.
admin.site.register(data_base,diagnosisAdmin)
