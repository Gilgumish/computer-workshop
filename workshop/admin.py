from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Component, Master, Client, Computer, Cart


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("email", "is_master", "is_client")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("is_master", "is_client")}),)
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


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ("user", "number_of_constructed_computers")
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(Computer)
class ComputerWorkshopAdmin(admin.ModelAdmin):
    list_display = ("name", "master", "pc_type", "price")
    search_fields = (
        "name",
        "master__user__username",
        "master__user__first_name",
        "master__user__last_name",
    )
    list_filter = ("pc_type",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("client", "total_price")
    search_fields = (
        "client__user__username",
        "client__user__first_name",
        "client__user__last_name",
    )

    def total_price(self, obj):
        return obj.total_price

    total_price.short_description = "Total Price"
