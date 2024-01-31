from django.urls import path

from .views import (AccountListAPI,
                    AccountCreateAPI,
                    AccountUpdateApi,
                    AccountDeleteAPI,
                    TransactionListAPI,
                    TransactionCreateAPI,
                    TransactionUpdateApi,
                    TransactionDeleteAPI)

ledger_patterns = [
    path('', AccountListAPI.as_view(), name='ledger_list'),
    path('transactions',
         TransactionListAPI.as_view(), name='ledger_transactions_list'),

    path('create', AccountCreateAPI.as_view(), name='ledger_create'),
    path('<int:account_id>/update',
         AccountUpdateApi.as_view(), name='ledger_update'),
    path('<int:account_id>/delete',
         AccountDeleteAPI.as_view(), name='ledger_delete'),

    path('<int:account_id>/transactions/create',
         TransactionCreateAPI.as_view(), name='ledger_transactions_create'),
    path('<int:account_id>/transactions/<int:transaction_id>/update',
         TransactionUpdateApi.as_view(), name='ledger_transactions_update'),
    path('<int:account_id>/transactions/<int:transaction_id>/delete',
         TransactionDeleteAPI.as_view(), name='ledger_transactions_delete'),
]
