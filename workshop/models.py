from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    is_master = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    number_of_constructed_computers = models.IntegerField(
        default=0, blank=True, null=True
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="workshop_user_set",
        blank=True,
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="workshop_user_set",
        blank=True,
        verbose_name="user permissions",
    )

    def save(self, *args, **kwargs):
        if self.is_master and self.is_client:
            raise ValidationError("User cannot be both master and client.")
        super().save(*args, **kwargs)


class Component(models.Model):
    TYPE_CHOICES = [
        ("CPU", "CPU"),
        ("GPU", "GPU"),
        ("RAM", "RAM"),
        ("Motherboard", "Motherboard"),
        ("PSU", "PSU"),
        ("Storage", "Storage"),
        ("Case", "Case"),
    ]

    name = models.CharField(max_length=100)
    specifications = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Computer(models.Model):
    PC_TYPE_CHOICES = [
        ("Gaming PC", "Gaming PC"),
        ("Workstation", "Workstation"),
        ("Office PC", "Office PC"),
        ("Mini PC", "Mini PC"),
        ("Server PC", "Server PC"),
        ("Media Center PC", "Media Center PC"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    components = models.ManyToManyField(Component)
    master = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_master": True}
    )
    pc_type = models.CharField(max_length=20, choices=PC_TYPE_CHOICES)

    @property
    def price(self):
        return sum(component.price for component in self.components.all())

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Cart(models.Model):
    client = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_client": True},
        related_name="client_cart",
    )
    components = models.ManyToManyField(Component, related_name="carts", blank=True)
    computers = models.ManyToManyField(Computer, related_name="carts", blank=True)
    master = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_master": True},
        related_name="master_carts",
    )

    def __str__(self):
        return f"Cart of {self.client.username}"

    @property
    def total_price(self):
        component_total = sum(item.price for item in self.components.all())
        computer_total = sum(comp.price for comp in self.computers.all())
        return component_total + computer_total
