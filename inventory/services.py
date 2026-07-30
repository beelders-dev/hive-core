from django.core.exceptions import ValidationError
from django.db import transaction


from .models import PurchaseAdjustment


class PurchaseAdjustmentService:

    STOCK_QTY_CANNOT_BE_NEGATIVE = "Adjustment cannot reduce stock below zero."

    @staticmethod
    @transaction.atomic
    def create(purchase, qty_adjustment, note):
        new_qty = qty_adjustment + purchase.total_stocks_plus_adjustments
        if new_qty < 0:
            raise ValidationError(
                PurchaseAdjustmentService.STOCK_QTY_CANNOT_BE_NEGATIVE
            )

        PurchaseAdjustment.objects.create(
            purchase=purchase,
            qty_adjustment=qty_adjustment,
            note=note,
        )
