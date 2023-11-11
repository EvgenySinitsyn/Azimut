from django.contrib.auth.models import Group
from django.db import models


class Counterparty(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    inn = models.CharField(max_length=30, verbose_name="ИНН", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        ordering = ["id"]


class Upd(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    date = models.DateField(verbose_name="Дата")
    number = models.IntegerField(verbose_name="Номер УПД", unique=True)
    counterparty = models.ForeignKey("Counterparty", on_delete=models.CASCADE, verbose_name="Контрагент")

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = "Услуга УПД"
        verbose_name_plural = "Услуги УПД"
        ordering = ["id"]


class Object(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование", unique=True)
    group = models.ManyToManyField(Group, verbose_name="Группа пользователя", through="ObjectGroup")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
        ordering = ["id"]


class Service(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    name = models.CharField(max_length=255, verbose_name="Наименование")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость")
    upd = models.ForeignKey("Upd", on_delete=models.CASCADE, verbose_name="УПД")
    object = models.ForeignKey("Object", on_delete=models.CASCADE, verbose_name="Объект")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["id"]


class Payment(models.Model):
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    date = models.DateField(verbose_name="Дата")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Размер платежа")
    counterparty = models.ForeignKey("Counterparty", on_delete=models.CASCADE, verbose_name="Контрагент")
    object = models.ForeignKey("Object", on_delete=models.CASCADE, verbose_name="Объект")

    def __str__(self):
        return str(self.amount)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["id"]


class ObjectGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа пользователя")
    object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name="Объект")
    fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Выплата")

    def __str__(self):
        return str(self.fee)

    class Meta:
        verbose_name = "Объект группы"
        verbose_name_plural = "Объекты групп"
        ordering = ["id"]
