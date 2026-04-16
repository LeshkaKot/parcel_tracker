from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class PostOffice(models.Model):
    number = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"№{self.number} - {self.city}"


class Parcel(models.Model):

    class Status(models.TextChoices):
        CREATED = 'created', 'Створено'
        ACCEPTED = 'accepted', 'Прийнято'
        IN_TRANSIT = 'in_transit', 'У дорозі'
        ARRIVED = 'arrived', 'Прибула'
        DELIVERED = 'delivered', 'Доставлено'
        RETURNED = 'returned', 'Повернуто'

    tracking_number = models.CharField(max_length=20, unique=True, editable=False)

    sender_name = models.CharField(max_length=100)
    sender_phone = models.CharField(max_length=20)

    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(30)]
    )

    declared_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    origin_office = models.ForeignKey(
        PostOffice,
        on_delete=models.PROTECT,
        related_name='sent_parcels'
    )
    destination_office = models.ForeignKey(
        PostOffice,
        on_delete=models.PROTECT,
        related_name='received_parcels'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = self._generate_tracking_number()
        super().save(*args, **kwargs)

    def _generate_tracking_number(self):
        random_track_num = uuid.uuid4().hex[:10].upper()
        return f"UA{random_track_num}"

    def __str__(self):
        return f"{self.tracking_number} ({self.status})"

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status', 'created_at']),
        ]


class ParcelStatusHistory(models.Model):
    parcel = models.ForeignKey(
        Parcel,
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    status = models.CharField(max_length=20, choices=Parcel.Status.choices)
    office = models.ForeignKey(
        PostOffice,
        on_delete=models.PROTECT,
        related_name='status_changes'
    )
    comment = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parcel.tracking_number} → {self.status}"