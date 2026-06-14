import uuid
from django.db import models


class TenantQuerySet(models.QuerySet):
    def for_organization(self, organization):
        return self.filter(organization=organization)


class TenantManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)

    def for_organization(self, organization):
        return self.get_queryset().for_organization(organization)


class TenantModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(
        'accounts.Organization',
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TenantManager()

    class Meta:
        abstract = True
