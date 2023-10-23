from django.contrib.auth.models import Group
from django.db import models


class Counterparty(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    inn = models.IntegerField(verbose_name="ИНН")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        ordering = ["id"]


class Upd(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    date = models.DateField(verbose_name="Дата")
    number = models.IntegerField(verbose_name="Номер УПД")
    counterparty = models.ForeignKey("Counterparty", on_delete=models.PROTECT, verbose_name="Контрагент")

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "УПД"
        verbose_name_plural = "УПД"
        ordering = ["id"]


class Service(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    price = models.FloatField(verbose_name="Стоимость")
    upd = models.ForeignKey("Upd", on_delete=models.PROTECT, verbose_name="УПД")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["id"]


class Payment(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    date = models.DateField(verbose_name="Дата")
    amount = models.FloatField(verbose_name="Стоимость")
    counterparty = models.ForeignKey("Counterparty", on_delete=models.PROTECT, verbose_name="Контрагент")
    object = models.ForeignKey("Object", on_delete=models.PROTECT, verbose_name="Объект")

    def __str__(self):
        return self.amount

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["id"]


class Object(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name="Группа пользователя")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
        ordering = ["id"]
