from .models import User, Address, CustomUser, Truck, Cargo, Delivery
from django.contrib.auth.admin import Group, UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .forms import CustomUserForm
from django.contrib import admin


class UserAdmin(BaseUserAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    list_filter = ()


class AddressAdmin(admin.ModelAdmin):
    def senders(self, obj):
        items = []
        result = ""
        for user in obj.sending_users.all():
            items.append(user.id)
            items.append(user.username)
            result += '<a href="/admin/alpha/customuser/{}/change/">{}</a> | '
        return format_html(result[:-3], *items)

    def receivers(self, obj):
        items = []
        result = ""
        for user in obj.receiving_users.all():
            items.append(user.id)
            items.append(user.username)
            result += '<a href="/admin/alpha/customuser/{}/change/">{}</a> | '
        return format_html(result[:-3], *items)

    def change_delete(self, obj):
        if obj.sending_users.exists() or obj.receiving_users.exists():
            return format_html(
                '<a class="changelink" href="/admin/alpha/address/{}/change/">Изменить</a>',
                obj.id,
            )
        else:
            return format_html(
                '<a class="changelink" href="/admin/alpha/address/{}/change/">Изменить</a> '
                '<a class="deletelink" href="/admin/alpha/address/{}/delete/">Удалить</a>',
                obj.id,
                obj.id,
            )

    def has_delete_permission(self, request, obj=None):
        return (
            obj and not obj.sending_users.exists() and not obj.receiving_users.exists()
        )

    list_display = (
        "id",
        "address",
        "senders",
        "receivers",
        "change_delete",
    )
    search_fields = ("address",)
    senders.short_description = "отправители"
    receivers.short_description = "получатели"
    change_delete.short_description = "действия"


class CustomUserAdmin(admin.ModelAdmin):
    def change_delete(self, obj):
        return format_html(
            '<a class="changelink" href="/admin/alpha/customuser/{}/change/">Изменить</a> '
            '<a class="deletelink" href="/admin/alpha/customuser/{}/delete/">Удалить</a>',
            obj.id,
            obj.id,
        )

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    list_display = (
        "id",
        "username",
        "phone_number",
        "type",
        "change_delete",
    )
    form = CustomUserForm
    search_fields = ("username", "phone_number")
    change_delete.short_description = "действия"


class TruckAdmin(admin.ModelAdmin):
    def change_delete(self, obj):
        return format_html(
            '<a class="changelink" href="/admin/alpha/truck/{}/change/">Изменить</a> '
            '<a class="deletelink" href="/admin/alpha/truck/{}/delete/">Удалить</a>',
            obj.id,
            obj.id,
        )

    list_display = (
        "id",
        "number",
        "datetime",
        "change_delete",
    )
    search_fields = ("number",)
    change_delete.short_description = "действия"


class CargoAdmin(admin.ModelAdmin):
    def change_delete(self, obj):
        return format_html(
            '<a class="changelink" href="/admin/alpha/cargo/{}/change/">Изменить</a> '
            '<a class="deletelink" href="/admin/alpha/cargo/{}/delete/">Удалить</a>',
            obj.id,
            obj.id,
        )

    list_display = (
        "id",
        "cargo_type",
        "change_delete",
    )
    search_fields = ("cargo_type",)
    change_delete.short_description = "действия"


class DeliveryAdmin(admin.ModelAdmin):
    def delete(self, obj):
        if obj.status == "Отправлен":
            return format_html(
                '<a class="deletelink" href="/admin/alpha/delivery/{}/delete/">Удалить</a>',
                obj.id,
            )
        else:
            return "поставка завершена"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return obj and obj.status == "Отправлен"

    list_display = (
        "status",
        "sent_at",
        "received_at",
        "transport_type",
        "transport_number",
        "cargo_type",
        "weight",
        "sending_address",
        "receiving_address",
        "sender",
        "receiver",
        "delete",
    )
    list_filter = ("status", "cargo_type")
    delete.short_description = "действия"


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Delivery, DeliveryAdmin)

admin.site.site_header = "Alpha Mining"
admin.site.site_title = "Администрирование"
admin.site.index_title = "Админ панель"
