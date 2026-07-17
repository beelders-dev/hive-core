from django.core.exceptions import ValidationError
from django.db import transaction


from .models import PurchaseAdjustment


class PurchaseAdjustmentService:

    @staticmethod
    @transaction.atomic
    def create(purchase, qty_adjustment, note):
        new_qty = qty_adjustment + purchase.total_stocks_plus_adjustments
        print(purchase)
        print(qty_adjustment)
        print(note)
        if new_qty < 0:
            raise ValidationError("Stock quantity cannot be negative.")

        PurchaseAdjustment.objects.create(
            purchase=purchase,
            qty_adjustment=qty_adjustment,
            note=note,
        )

        return purchase
