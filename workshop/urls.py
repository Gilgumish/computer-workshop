from django.urls import path
from .views import (
    home,
    login_view,
    register_view,
    configurator,
    edit_component,
    delete_component,
    manage_users,
    add_computer,
    add_component,
    ComputerDeleteView,
    ComponentDeleteView,
    edit_computer,
    edit_user,
    computer_detail,
    AvailableComputersView,
    AvailableComponentsView,
    view_cart,
    remove_from_cart,
    add_component_to_cart,
    add_computer_to_cart,
    clear_cart,
    remove_master_from_cart, view_user_cart,
)

app_name = "workshop"

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path(
        "available_computers/",
        AvailableComputersView.as_view(),
        name="available_computers",
    ),
    path("configurator/", configurator, name="configurator"),
    path("edit_component/<int:component_id>/", edit_component, name="edit_component"),
    path(
        "delete_component/<int:component_id>/",
        delete_component,
        name="delete_component",
    ),
    path("components/", AvailableComponentsView.as_view(), name="components_list"),
    path("manage_users/", manage_users, name="manage_users"),
    path("add_computer/", add_computer, name="add_computer"),
    path("add_component/", add_component, name="add_component"),
    path("edit_computer/<int:computer_id>/", edit_computer, name="edit_computer"),
    path(
        "delete_computer/<int:pk>/",
        ComputerDeleteView.as_view(),
        name="delete_computer",
    ),
    path(
        "delete_component/<int:pk>/",
        ComponentDeleteView.as_view(),
        name="delete_component",
    ),
    path("edit_user/<int:user_id>/", edit_user, name="edit_user"),
    path("computer_detail/<int:pk>/", computer_detail, name="computer_detail"),
    path("cart/", view_cart, name="cart"),
    path('user_cart/<int:client_id>/', view_user_cart, name='view_user_cart'),
    path(
        "cart/add_component/<int:component_id>/",
        add_component_to_cart,
        name="add_component_to_cart",
    ),
    path(
        "cart/add_computer/<int:computer_id>/",
        add_computer_to_cart,
        name="add_computer_to_cart",
    ),
    path(
        "cart/remove/<int:item_id>/<str:item_type>/",
        remove_from_cart,
        name="remove_from_cart",
    ),
    path("cart/clear/", clear_cart, name="clear_cart"),
    path(
        "cart/remove_master/", remove_master_from_cart, name="remove_master_from_cart"
    ),
]
