import django_filters

from flowback.user.models import User
from flowback_addon.ledger.models import Account, Transaction


class BaseAccountFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(('created_at', 'created_at_asc'),
                ('-created_at', 'created_at_desc'))
    )

    class Meta:
        model = Account
        fields = dict(id=['exact'],)


def account_list(*, user: User, filters=None):
    filters = filters or {}

    qs = Account.objects.filter(user=user).all()
    return BaseAccountFilter(filters, qs).qs


class BaseTransactionFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(('created_at', 'created_at_asc'),
                ('-created_at', 'created_at_desc'),
                ('date', 'date_asc'),
                ('-date', 'date_desc'))
    )

    class Meta:
        model = Transaction
        fields = dict(id=['exact'],)


def transaction_list(*, user: User, filters=None):
    filters = filters or {}

    qs = Transaction.objects.filter(account__user=user).all()
    return BaseTransactionFilter(filters, qs).qs
