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

    description = django_filters.CharFilter(
        field_name='description',
        lookup_expr='icontains' 
    )

    account_ids = django_filters.CharFilter(
        method='filter_by_accounts'
    )

    def filter_by_accounts(self, queryset, name, value):
        account_ids = value.split(',')  # Split the value by comma to get a list of account IDs
        print(account_ids)
        return queryset.filter(account__id__in=account_ids)

    class Meta:
        model = Transaction
        fields = {
            'id': ['exact'],
            # 'account_ids': [],
            'description': ['icontains'],
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

