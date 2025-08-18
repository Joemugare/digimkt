# affiliate/admin.py
from django.contrib import admin
from .models import AffiliateProgram, AffiliateLink, LinkClick

@admin.register(AffiliateProgram)
class AffiliateProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'commission_rate', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'company')

@admin.register(AffiliateLink)
class AffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'category', 'click_count', 'conversion_rate', 'is_active')
    list_filter = ('category', 'is_active', 'program')
    search_fields = ('title',)

@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = ('link', 'ip_address', 'click_date')
    list_filter = ('click_date',)
    search_fields = ('ip_address',)