from django.contrib import admin

from sites.models import Site,SiteLog

class SiteLogInline(admin.TabularInline):
    model = SiteLog
    extra = 0
    max_num = 10

class SiteAdmin(admin.ModelAdmin):
    list_display = ['__str__']
    inlines = [
        SiteLogInline,
    ]
    class Meta:
        model = Site
admin.site.register(Site, SiteAdmin)