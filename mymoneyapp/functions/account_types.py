from ..models import AccountType

def populate_types():
    AccountType.objects.update_or_create(
        id = 1, acc_type = "General"
    )

    AccountType.objects.update_or_create(
        id = 2, acc_type = "Efectivo"
    )

    AccountType.objects.update_or_create(
        id = 3, acc_type = "Ahorros"
    )

    AccountType.objects.update_or_create(
        id = 4, acc_type = "Tarjeta"
    )