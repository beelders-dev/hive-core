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
