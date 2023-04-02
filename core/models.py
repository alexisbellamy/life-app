from django.db import models


class Category(models.Model):
    name=models.CharField(max_length=255)
    icon=models.CharField(max_length=255)


class Item(models.Model):
    name=models.CharField(max_length=255)
    value=models.CharField(max_length=255)
    # type=models.CharField(max_length=255)


class ItemCategory(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    item=models.ForeignKey(Item, on_delete=models.CASCADE)
