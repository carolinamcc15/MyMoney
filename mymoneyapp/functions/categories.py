from ..models import Category

def populate_categories():
    Category.objects.update_or_create(
        id = 1, category = "Comida y bebida"
    )

    Category.objects.update_or_create(
        id = 2, category = "Compras"
    )

    Category.objects.update_or_create(
        id = 3, category = "Vivienda"
    )

    Category.objects.update_or_create(
        id = 4, category = "Transporte"
    )

    Category.objects.update_or_create(
        id = 5, category = "Entretenimiento"
    )

    Category.objects.update_or_create(
        id = 6, category = "Comunicaciones"
    )

    Category.objects.update_or_create(
        id = 7, category = "Ingreso"
    )

    Category.objects.update_or_create(
        id = 8, category = "Inversiones"
    )

    Category.objects.update_or_create(
        id = 9, category = "Otros"
    )