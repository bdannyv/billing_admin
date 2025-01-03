import uuid

from django.db import models

BILLING_SCHEMA = "billing"


class IDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=True)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{BILLING_SCHEMA}"."client"'
        verbose_name = "Client"
        unique_together = ("name", "number")

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}, #{self.number}"


class Payer(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{BILLING_SCHEMA}"."payer"'
        verbose_name = "Payer"
        unique_together = ("name", "number")

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    clients = models.ManyToManyField(Client, through="ClientPayer", related_name="payers")

    def __str__(self):
        return f"{self.name}, #{self.number}"


class ClientPayer(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{BILLING_SCHEMA}"."client_payer"'
        verbose_name = "Client <-> Payer mapping"

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Client {self.client_id} <-> Payer {self.payer_id}"


class Matter(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{BILLING_SCHEMA}"."matter"'
        verbose_name = "Matter"
        unique_together = ("title", "number")

    title = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    matter_actor = models.ForeignKey("Actor", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.title}"


class Actor(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{BILLING_SCHEMA}"."actor"'
        verbose_name = "Actor"
        unique_together = ("name", "number")

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Bill(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{BILLING_SCHEMA}"."billing"'
        verbose_name = "Billing"
        unique_together = ("title", "number")

    title = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    bill_actor = models.ForeignKey(Actor, on_delete=models.PROTECT)

    def __str__(self):
        return f"Bill #{self.number}. {self.title}"


class ActionCode(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{BILLING_SCHEMA}"."action_code"'
        unique_together = ("code", "classification")

    code = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code}. {self.description}"


class Action(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{BILLING_SCHEMA}"."action"'
        verbose_name = "Action"
        unique_together = ("title", "number")

    title = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    code = models.ForeignKey(ActionCode, on_delete=models.PROTECT)
    time = models.IntegerField(db_comment="Time spent on the activity, seconds")
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.number}. {self.title}"
