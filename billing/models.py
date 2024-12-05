from django.db import models

BILLING_SCHEMA = "billing"


class IDMixin(models.Model):
    id = models.UUIDField(primary_key=True)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f"{BILLING_SCHEMA}.client"
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        unique_together = ("name", "number")

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)

    def __str__(self):
        return f"Client: {self.name}, #{self.number}"


class Payer(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f"{BILLING_SCHEMA}.payer"
        verbose_name = "Payer"
        verbose_name_plural = "Payers"
        unique_together = ("name", "number")

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    clients = models.ManyToManyField(Client, through="ClientPayer", related_name="payers")

    def __str__(self):
        return f"Payer: {self.name}, #{self.number}"


class ClientPayer(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f"{BILLING_SCHEMA}.client_payer"

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    payer = models.ForeignKey(Payer, on_delete=models.CASCADE)


class Matter(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f"{BILLING_SCHEMA}.matter"
        verbose_name = "Matter"
        verbose_name_plural = "Matters"
        unique_together = ("title", "number")

    title = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)


class Actor(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f"{BILLING_SCHEMA}.actor"
        verbose_name = "Actor"
        verbose_name_plural = "Actors"
        unique_together = ("name", "number")

    name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)


class Bill(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f"{BILLING_SCHEMA}.billing"
        verbose_name = "Billing"
        verbose_name_plural = "Billings"
        unique_together = ("title", "number")

    title = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    billing_actor = models.ForeignKey(Actor, on_delete=models.PROTECT)


class ActionCode(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f"{BILLING_SCHEMA}.action_code"
        unique_together = ("code", "classification")

    code = models.CharField(max_length=255)
    classification = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


class Action(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f"{BILLING_SCHEMA}.action"
        verbose_name = "Action"
        verbose_name_plural = "Actions"
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
