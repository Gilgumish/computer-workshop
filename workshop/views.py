from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView

from .models import Computer, Component, Cart, User
from .forms import (
    ComponentForm,
    ConfiguratorForm,
    CustomUserCreationForm,
    ComputerForm,
    UserForm,
    AddComponentToCartForm,
    AddComputerToCartForm,
)


def home(request):
    num_computers = Computer.objects.count()
    num_components = Component.objects.count()
    num_masters = User.objects.filter(is_master=True).count()

    return render(
        request,
        "workshop/index.html",
        {
            "num_computers": num_computers,
            "num_components": num_components,
            "num_masters": num_masters,
        },
    )


class AvailableComputersView(ListView):
    model = Computer
    template_name = "workshop/available_computers.html"
    context_object_name = "computers"
    paginate_by = 9

    def get_queryset(self):
        sort_by = self.request.GET.get("sort_by", "name")
        pc_type = self.request.GET.get("pc_type", "")
        search_query = self.request.GET.get("search", "")

        queryset = Computer.objects.all()

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        if pc_type:
            queryset = queryset.filter(pc_type=pc_type)

        if sort_by == "name":
            queryset = queryset.order_by("name")
        elif sort_by == "type":
            queryset = queryset.order_by("pc_type")
        elif sort_by == "price":
            queryset = sorted(queryset, key=lambda c: c.price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort_by", "name")
        context["pc_type"] = self.request.GET.get("pc_type", "")
        context["search_query"] = self.request.GET.get("search", "")
        context["pc_types"] = Computer.PC_TYPE_CHOICES
        return context


def computer_detail(request, pk):
    computer = get_object_or_404(Computer, pk=pk)
    return render(request, "workshop/computer_detail.html", {"computer": computer})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("workshop:home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("workshop:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def configurator(request):
    if request.method == "POST":
        form = ConfiguratorForm(request.POST)
        if form.is_valid():
            cart, created = Cart.objects.get_or_create(client=request.user)
            cart.components.add(form.cleaned_data["cpu"])
            cart.components.add(form.cleaned_data["gpu"])
            cart.components.add(form.cleaned_data["ram"])
            cart.components.add(form.cleaned_data["motherboard"])
            cart.components.add(form.cleaned_data["psu"])
            for storage in form.cleaned_data["storage"]:
                cart.components.add(storage)
            cart.components.add(form.cleaned_data["case"])
            cart.master = form.cleaned_data["master"]
            cart.save()
            return redirect("workshop:cart")
    else:
        form = ConfiguratorForm()

    return render(request, "workshop/configurator.html", {"form": form})


@login_required
def add_computer(request):
    if not request.user.is_master:
        return redirect("workshop:home")
    if request.method == "POST":
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("workshop:available_computers")
    else:
        form = ComputerForm()
    return render(request, "workshop/add_computer.html", {"form": form})


class AvailableComponentsView(ListView):
    model = Component
    template_name = "workshop/components_list.html"
    context_object_name = "components"
    paginate_by = 9

    def get_queryset(self):
        sort_by = self.request.GET.get("sort_by", "name")
        component_type = self.request.GET.get("component_type", "")
        search_query = self.request.GET.get("search", "")

        queryset = Component.objects.all()

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        if component_type:
            queryset = queryset.filter(type=component_type)

        if sort_by == "name":
            queryset = queryset.order_by("name")
        elif sort_by == "type":
            queryset = queryset.order_by("type")
        elif sort_by == "price":
            queryset = queryset.order_by("price")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort_by", "name")
        context["component_type"] = self.request.GET.get("component_type", "")
        context["search_query"] = self.request.GET.get("search", "")
        context["component_types"] = Component.TYPE_CHOICES
        return context


@login_required
def view_user_cart(request, user_id):
    if not request.user.is_master:
        return redirect("workshop:home")

    user = get_object_or_404(User, id=user_id)
    if not user.is_client:
        return redirect("workshop:home")

    cart, created = Cart.objects.get_or_create(client=user)
    return render(request, "workshop/user_cart.html", {"cart": cart, "client": user})


@login_required
def manage_users(request):
    if not request.user.is_superuser and not request.user.is_master:
        return redirect("workshop:home")

    search_query = request.GET.get("search", "")
    master_filter = request.GET.get("is_master", "")

    users = User.objects.all()

    if search_query:
        users = users.filter(username__icontains=search_query)

    if master_filter:
        if master_filter.lower() == "yes":
            users = users.filter(is_master=True)
        elif master_filter.lower() == "no":
            users = users.filter(is_master=False)

    user_data = []
    for user in users:
        assembled_pcs_count = (
            user.number_of_constructed_computers if user.is_master else "-"
        )
        user_data.append({"user": user, "assembled_pcs_count": assembled_pcs_count})

    paginator = Paginator(user_data, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "workshop/manage_users.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
            "master_filter": master_filter,
        },
    )


@login_required
def edit_component(request, component_id):
    if not request.user.is_master:
        return redirect("workshop:home")

    component = get_object_or_404(Component, id=component_id)
    if request.method == "POST":
        form = ComponentForm(request.POST, instance=component)
        if form.is_valid():
            form.save()
            return redirect("workshop:components_list")
    else:
        form = ComponentForm(instance=component)

    return render(request, "workshop/edit_component.html", {"form": form})


@login_required
def delete_component(request, component_id):
    if not request.user.is_master:
        return redirect("workshop:home")

    component = get_object_or_404(Component, id=component_id)

    if request.method == "POST":
        component.delete()
        return redirect("workshop:components_list")

    return render(
        request, "workshop/component_confirm_delete.html", {"component": component}
    )


@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser:
        return redirect("workshop:home")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("workshop:manage_users")
    else:
        form = UserForm(instance=user)

    return render(request, "workshop/edit_user.html", {"form": form, "user": user})


@login_required
def add_component(request):
    if not request.user.is_master:
        return redirect("workshop:home")
    if request.method == "POST":
        form = ComponentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("workshop:components_list")
    else:
        form = ComponentForm()
    return render(request, "workshop/add_component.html", {"form": form})


@login_required
def edit_computer(request, computer_id):
    if not request.user.is_master:
        return redirect("workshop:home")

    computer = get_object_or_404(Computer, id=computer_id)
    if request.method == "POST":
        form = ComputerForm(request.POST, instance=computer)
        if form.is_valid():
            form.save()
            return redirect("workshop:available_computers")
    else:
        form = ComputerForm(
            instance=computer,
            initial={
                "cpu": computer.components.filter(type="CPU").first(),
                "gpu": computer.components.filter(type="GPU").first(),
                "ram": computer.components.filter(type="RAM").first(),
                "motherboard": computer.components.filter(type="Motherboard").first(),
                "psu": computer.components.filter(type="PSU").first(),
                "storage": computer.components.filter(type="Storage"),
                "case": computer.components.filter(type="Case").first(),
            },
        )

    return render(
        request, "workshop/add_computer.html", {"form": form, "object": computer}
    )


class ComputerDeleteView(DeleteView):
    model = Computer
    template_name = "workshop/computer_confirm_delete.html"
    success_url = reverse_lazy("workshop:home")


class ComponentDeleteView(DeleteView):
    model = Component
    template_name = "workshop/component_confirm_delete.html"
    success_url = reverse_lazy("workshop:master_dashboard")


@login_required
def add_component_to_cart(request, component_id):
    component = get_object_or_404(Component, id=component_id)
    cart, created = Cart.objects.get_or_create(client=request.user)

    cart.components.add(component)
    return redirect("workshop:cart")


@login_required
def add_computer_to_cart(request, computer_id):
    computer = get_object_or_404(Computer, id=computer_id)
    cart, created = Cart.objects.get_or_create(client=request.user)

    cart.computers.add(computer)
    return redirect("workshop:cart")


@login_required
def view_cart(request):
    if not request.user.is_client:
        return redirect("workshop:home")

    cart, created = Cart.objects.get_or_create(client=request.user)
    return render(request, "workshop/cart.html", {"cart": cart})


@login_required
def remove_from_cart(request, item_id, item_type):
    cart, created = Cart.objects.get_or_create(client=request.user)
    if item_type == "component":
        item = get_object_or_404(Component, id=item_id)
        cart.components.remove(item)
    elif item_type == "computer":
        item = get_object_or_404(Computer, id=item_id)
        cart.computers.remove(item)
    return redirect("workshop:cart")


@login_required
def clear_cart(request):
    cart, created = Cart.objects.get_or_create(client=request.user)
    cart.components.clear()
    cart.computers.clear()
    cart.master = None
    cart.save()
    return redirect("workshop:cart")


@login_required
def remove_master_from_cart(request):
    cart, created = Cart.objects.get_or_create(client=request.user)
    cart.master = None
    cart.save()
    return redirect("workshop:cart")
