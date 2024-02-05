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
        fields = {
            'id': ['exact'],
        }


def account_list(*, user: User, filters=None):
    filters = filters or {}

    qs = Account.objects.filter(user=user).all()

    filtered_qs = BaseAccountFilter(filters, qs).qs

    return filtered_qs


class BaseTransactionFilter(django_filters.FilterSet):
    order_by = django_filters.OrderingFilter(
        fields=(('created_at', 'created_at_asc'),
                ('-created_at', 'created_at_desc'),
                ('date', 'date_asc'),
                ('-date', 'date_desc'))
    )

    date_after = django_filters.DateFilter(field_name='date', lookup_expr='gt')
    date_before = django_filters.DateFilter(field_name='date', lookup_expr='lt')

    class Meta:
        model = Transaction
        fields = {
            'id': ['exact'],
            'account_id': ['exact'],
        }
        extra = {
            'date_after': {'lookup_expr': 'gt'},
            'date_before': {'lookup_expr': 'lt'},
        }
        


# Modify the transaction_list function
def transaction_list(*, user: User, filters=None):
    filters = filters or {}

    qs = Transaction.objects.filter().all()

    # Apply custom filters using BaseTransactionFilter
    filtered_qs = BaseTransactionFilter(filters, qs).qs

    return filtered_qs

