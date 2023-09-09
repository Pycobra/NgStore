from django.contrib import admin

from .models import Vendor, Follow, VendorImages, VendorImageValue, SubscriptionType, Subscriptions
from mptt.admin import MPTTModelAdmin

@admin.register(VendorImages)
class VendorImagesAdmin(admin.ModelAdmin):
    pass


class VendorImageValueInline(admin.TabularInline):
    model = VendorImageValue


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    inlines = [VendorImageValueInline,]
    list_display = ['store_name', 'created_at']
    #prepopulated_fields = {'slug',('name',)}
    """list_filter =
    list_display_links =
    list_per_page =
    list_select_related =
    list_max_show_all =
    preserve_filters =
    paginator =
    actions =
    actions_on_top =
    action_form =
    change_list_template =
    change_form_template =
    checks_class =
    date_hierarchy =
    delete_confirmation_template =
    delete_selected_confirmation_template =
    exclude =
    filter_vertical =
    filter_horizontal =
    inlines =
    object_history_template =
    popup_response_template =
    prepopulated_fields =
    radio_fields =
    readonly_fields =
    raw_id_fields =
    search_fields =
    save_as =
    save_on_top =
    sortable_by =
    save_as_continue =
    show_full_result_count =
    view_on_site ="""
admin.site.register(Follow)

admin.site.register(SubscriptionType)

admin.site.register(Subscriptions)


