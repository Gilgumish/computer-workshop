from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Component, Computer, Cart


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "email",
        "is_master",
        "is_client",
        "number_of_constructed_computers",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "is_master",
                        "is_client",
                        "number_of_constructed_computers",
                    )
                },
            ),
        )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "email",
                        "is_master",
                        "is_client",
                        "number_of_constructed_computers",
                    )
                },
            ),
        )
    )


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price")
    search_fields = ("name", "type")
    list_filter = ("type",)


@admin.register(Computer)
class ComputerWorkshopAdmin(admin.ModelAdmin):
    list_display = ("name", "master", "pc_type", "price")
    search_fields = (
        "name",
        "master__username",
        "master__first_name",
        "master__last_name",
    )
    list_filter = ("pc_type",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("client", "total_price")
    search_fields = (
        "client__username",
        "client__first_name",
        "client__last_name",
    )

    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = "Total Price"
