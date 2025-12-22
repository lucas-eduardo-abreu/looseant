from django.contrib import admin

from looseinventory.inventory.models import HaveListItem, Item, SpecifiedItem, WantListItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "created_at"]


@admin.register(SpecifiedItem)
class SpecifiedItemAdmin(admin.ModelAdmin):
    list_display = ["item", "mh", "sd", "dd", "ref", "dsr", "zen", "created_at"]
    list_filter = ["mh", "sd", "dd", "ref", "dsr", "zen"]
    search_fields = ["item__name"]


@admin.register(WantListItem)
class WantListItemAdmin(admin.ModelAdmin):
    list_display = ["user", "specified_item", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["user__username", "specified_item__item__name"]


@admin.register(HaveListItem)
class HaveListItemAdmin(admin.ModelAdmin):
    list_display = ["user", "specified_item", "created_at"]
    search_fields = ["user__username", "specified_item__item__name"]
