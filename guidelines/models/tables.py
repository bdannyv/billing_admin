import uuid

from django.db import models

GUIDELINE_SCHEMA = "guideline"


class IDMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=True)


class TimestampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Guideline(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."guideline"'
        verbose_name = "Guideline"
        verbose_name_plural = "Guidelines"

    name = models.CharField(max_length=255)
    payers = models.ManyToManyField("billing.Payer", through="GuidelinePayer")
    matter = models.ManyToManyField("billing.Matter", through="GuidelineMatter")
    client = models.ManyToManyField("billing.Client", through="GuidelineClient")
    actors = models.ManyToManyField("billing.Actor", through="GuidelineActor")
    firmwide = models.BooleanField(default=False)

    def __str__(self):
        return f"Guideline: {self.name}"


class GuidelinePayer(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."guideline_payer"'
        verbose_name = "Guideline <-> Payer"
        verbose_name_plural = "Guideline <-> Payer mapping"
        unique_together = ("guideline", "payer")

    guideline = models.ForeignKey("Guideline", on_delete=models.CASCADE)
    payer = models.ForeignKey("billing.Payer", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Guideline: {self.guideline} <-> Payer {self.payer}"


class GuidelineMatter(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."guideline_matter"'
        verbose_name = "Guideline <-> Matter"
        verbose_name_plural = "Guideline <-> Matter Mapping"
        unique_together = ("guideline", "matter")

    guideline = models.ForeignKey("Guideline", on_delete=models.CASCADE)
    matter = models.ForeignKey("billing.Matter", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Guideline: {self.guideline} <-> Matter {self.matter}"


class GuidelineClient(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."guideline_client"'
        verbose_name = "Guideline <-> Client"
        verbose_name_plural = "Guideline <-> Client Mapping"
        unique_together = ("guideline", "client")

    guideline = models.ForeignKey("Guideline", on_delete=models.CASCADE)
    client = models.ForeignKey("billing.Client", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Guideline {self.guideline} <-> Client {self.client}"


class GuidelineActor(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."guideline_actor"'
        verbose_name = "Guideline <-> Actor"
        verbose_name_plural = "Guideline <-> Client Mapping"
        unique_together = ("guideline", "actor")

    guideline = models.ForeignKey("Guideline", on_delete=models.CASCADE)
    actor = models.ForeignKey("billing.Actor", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Guideline {self.guideline} <-> Actor {self.actor}"


class Rule(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."rule"'
        verbose_name = "Rule"
        verbose_name_plural = "Rules"

    title = models.CharField(max_length=255)
    guideline = models.ForeignKey(Guideline, on_delete=models.SET_NULL, null=True, blank=True)
    firmwide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class RulePayer(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."rule_payer"'
        verbose_name = "Rule <-> Payer"
        verbose_name_plural = "Rule <-> Payer mapping"
        unique_together = ("rule", "payer")

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    payer = models.ForeignKey("billing.Payer", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Guideline: {self.rule} <-> Matter {self.payer}"


class RuleMatter(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."rule_matter"'
        verbose_name = "Rule <-> Matter"
        verbose_name_plural = "Rule <-> Matter Mapping"
        unique_together = ("rule", "matter")

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    matter = models.ForeignKey("billing.Matter", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Guideline: {self.rule} <-> Matter {self.matter}"


class RuleClient(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."rule_client"'
        verbose_name = "Rule <-> Client"
        verbose_name_plural = "Rule <-> Client Mapping"
        unique_together = ("rule", "client")

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    client = models.ForeignKey("billing.Client", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Guideline {self.rule} <-> Client {self.client}"


class RuleActor(IDMixin, TimestampMixin, models.Model):
    class Meta:
        db_table = f'"{GUIDELINE_SCHEMA}"."rule_actor"'
        verbose_name = "Rule <-> Actor"
        verbose_name_plural = "Rule <-> Client Mapping"
        unique_together = ("rule", "actor")

    rule = models.ForeignKey(Rule, on_delete=models.CASCADE)
    actor = models.ForeignKey("billing.Actor", on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Guideline {self.rule} <-> Actor {self.actor}"
