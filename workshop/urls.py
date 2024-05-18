from django.urls import path
from .views import (
    home,
    login_view,
    register_view,
    configurator,
    add_to_cart,
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
    path("add_to_cart/<int:computer_id>/", add_to_cart, name="add_to_cart"),
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
]
