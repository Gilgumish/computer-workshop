from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView

from .models import Computer, Component, Cart, Client, User, Master
from .forms import (
    ComponentForm,
    ConfiguratorForm,
    CustomUserCreationForm,
    ComputerForm,
    UserForm,
)


def home(request):
    num_computers = Computer.objects.count()
    num_components = Component.objects.count()
    num_masters = Master.objects.count()

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
            computer = form.save(commit=False)
            computer.master = Master.objects.get(user=request.user)
            computer.save()
            return redirect("workshop:home")
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


@login_required
def add_to_cart(request, computer_id):
    computer = get_object_or_404(Computer, id=computer_id)
    client = get_object_or_404(Client, user=request.user)
    cart, created = Cart.objects.get_or_create(client=client)
    cart.items.add(computer)
    return redirect("workshop:home")


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
def manage_users(request):
    if not request.user.is_superuser:
        return redirect("workshop:home")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("workshop:manage_users")

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
        if user.is_master:
            assembled_pcs_count = Computer.objects.filter(master=user.master).count()
        else:
            assembled_pcs_count = "-"
        user_data.append({"user": user, "assembled_pcs_count": assembled_pcs_count})

    return render(
        request,
        "workshop/manage_users.html",
        {
            "user_data": user_data,
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
        # Populate the form with the initial data
        form = ComputerForm(instance=computer, initial={
            'cpu': computer.components.filter(type='CPU').first(),
            'gpu': computer.components.filter(type='GPU').first(),
            'ram': computer.components.filter(type='RAM').first(),
            'motherboard': computer.components.filter(type='Motherboard').first(),
            'psu': computer.components.filter(type='PSU').first(),
            'storage': computer.components.filter(type='Storage'),
            'case': computer.components.filter(type='Case').first(),
        })

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
