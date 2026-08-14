from django.urls import reverse


def ingredient_detail_tabs(ingredient):
    return [
        {
            "id": "overview",
            "label": "Overview",
            "url": reverse(
                "inventory:ingredient_overview",
                kwargs={"pk": ingredient.pk},
            ),
        },
        {
            "id": "purchases",
            "label": "Purchases",
            "url": reverse(
                "inventory:purchase_list",
                kwargs={"pk": ingredient.pk},
            ),
        },
    ]


def purchase_detail_tabs(purchase):
    return [
        {
            "id": "overview",
            "label": "Overview",
            "url": reverse(
                "inventory:purchase_overview",
                kwargs={"pk": purchase.pk},
            ),
        },
        {
            "id": "adjustments",
            "label": "Adjustments",
            "url": reverse(
                "inventory:adjustment_list",
                kwargs={"pk": purchase.pk},
            ),
        },
    ]
