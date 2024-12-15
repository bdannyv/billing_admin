from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Q

DELEGATION_SCHEMA = "delegation"


class UserActor(models.Model):
    class Meta:
        db_table = f"{DELEGATION_SCHEMA}.user_actor"
        constraints = [models.CheckConstraint(check=Q(period_end__gt=F("period_start")), name="period_end_start_check")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    actor = models.ForeignKey("billing.Actor", on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
