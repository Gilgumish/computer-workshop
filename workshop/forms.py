from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Component, Computer, Master, User


class UserForm(forms.ModelForm):
    number_of_constructed_computers = forms.IntegerField(
        required=False,
        label="Number of PCs Built",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.is_master:
            self.fields["number_of_constructed_computers"].initial = (
                self.instance.master.number_of_constructed_computers
            )
        else:
            self.fields.pop("number_of_constructed_computers")

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.is_master:
            master, created = Master.objects.get_or_create(user=user)
            master.number_of_constructed_computers = self.cleaned_data.get(
                "number_of_constructed_computers",
                master.number_of_constructed_computers,
            )
            if commit:
                master.save()
        if commit:
            user.save()
        return user


class BaseComputerForm(forms.ModelForm):
    cpu = forms.ModelChoiceField(
        queryset=Component.objects.filter(type="CPU"),
        required=True,
        label="CPU",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    gpu = forms.ModelChoiceField(
        queryset=Component.objects.filter(type="GPU"),
        required=True,
        label="GPU",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    ram = forms.ModelChoiceField(
        queryset=Component.objects.filter(type="RAM"),
        required=True,
        label="RAM",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    motherboard = forms.ModelChoiceField(
        queryset=Component.objects.filter(type="Motherboard"),
        required=True,
        label="Motherboard",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    psu = forms.ModelChoiceField(
        queryset=Component.objects.filter(type="PSU"),
        required=True,
        label="PSU",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    storage = forms.ModelMultipleChoiceField(
        queryset=Component.objects.filter(type="Storage"),
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )
    case = forms.ModelChoiceField(
        queryset=Component.objects.filter(type="Case"),
        required=True,
        label="Case",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["cpu", "gpu", "ram", "motherboard", "psu", "case"]:
            if field_name in ["motherboard", "case"]:
                self.fields[field_name].queryset = Component.objects.filter(
                    type=field_name.capitalize()
                )
            else:
                self.fields[field_name].queryset = Component.objects.filter(
                    type=field_name.upper()
                )
            self.fields[field_name].label_from_instance = (
                lambda obj: f"{obj.name} (${obj.price})"
            )

        self.fields["storage"].queryset = Component.objects.filter(type="Storage")
        self.fields["storage"].label_from_instance = (
            lambda obj: f"{obj.name} (${obj.price})"
        )


class ConfiguratorForm(BaseComputerForm):
    master = forms.ModelChoiceField(
        queryset=Master.objects.all(),
        required=True,
        label="Select a Master",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Computer
        fields = [
            "cpu",
            "gpu",
            "ram",
            "motherboard",
            "psu",
            "storage",
            "case",
            "master",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["master"].queryset = Master.objects.all()
        self.fields["master"].label_from_instance = (
            lambda obj: f"{obj.user.first_name} '{obj.user.username}' {obj.user.last_name} (PCs Built: {obj.number_of_constructed_computers})"
        )


class ComputerForm(BaseComputerForm):
    class Meta:
        model = Computer
        fields = [
            "name",
            "description",
            "pc_type",
            "cpu",
            "gpu",
            "ram",
            "motherboard",
            "psu",
            "storage",
            "case",
        ]

    def save(self, commit=True, user=None):
        computer = super().save(commit=False)
        if user and hasattr(user, "master"):
            computer.master = user.master
            user.master.number_of_constructed_computers += 1
            user.master.save()
        if commit:
            computer.save()
            computer.components.set(
                [
                    self.cleaned_data["cpu"],
                    self.cleaned_data["gpu"],
                    self.cleaned_data["ram"],
                    self.cleaned_data["motherboard"],
                    self.cleaned_data["psu"],
                    *self.cleaned_data["storage"],
                    self.cleaned_data["case"],
                ]
            )
        return computer


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ["name", "specifications", "price", "type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "specifications": forms.Textarea(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Required. Inform a valid email address."
    )
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional.")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class AddComponentToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    )

    class Meta:
        model = Component
        fields = ["quantity"]


class AddComputerToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
    )

    class Meta:
        model = Computer
        fields = ["quantity"]
