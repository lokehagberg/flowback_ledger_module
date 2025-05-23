from datetime import datetime

from flowback.common.services import model_update, get_object
from .models import Account, Transaction
from flowback.user.models import User


def account_create(*, user_id: int, account_number: str, account_name: str) -> Account:
    user = get_object(User, id=user_id)
    account = Account(account_number=account_number,
                      account_name=account_name,
                      user=user)

    account.full_clean()
    account.save()

    return account


def account_update(user_id: int, account_id: int, data) -> Account:
    user = get_object(User, id=user_id)
    account = get_object(Account, id=account_id, user=user)

    data['updated_at'] = datetime.now()
    non_side_effect_fields = ['account_number', 'account_name', 'updated_at']
    account, has_updated = model_update(instance=account,
                                        fields=non_side_effect_fields,
                                        data=data)
    return account


def account_delete(user_id: int, account_id: int):
    user = get_object(User, id=user_id)
    account = get_object(Account, id=account_id, user=user)
    account.delete()


def transaction_create(*,
                       user_id: int,
                       debit_amount: float = 0,
                       credit_amount: float = 0,
                       description: str,
                       verification_number: str,
                       account_id: int,
                       date: str = datetime.now()) -> Transaction:
    user = get_object(User, id=user_id)
    account = get_object(Account, id=account_id, user=user)

    transaction = Transaction(
        account=account,
        debit_amount=debit_amount,
        credit_amount=credit_amount,
        description=description,
        verification_number=verification_number,
        date=date
    )

    transaction.full_clean()
    transaction.save()

    return transaction


def transaction_update(user_id: int, transaction_id: int, data) -> Account:
    user = get_object(User, id=user_id)
    transaction = get_object(Transaction, id=transaction_id, account__user=user)

    if 'debit_amount' in data:
        data['credit_amount'] = 0
    else:
        data['debit_amount'] = 0

    data['updated_at'] = datetime.now()
    non_side_effect_fields = [
        'debit_amount', 'credit_amount', 'description', 'verification_number', 'date', 'updated_at']
    transaction, has_updated = model_update(instance=transaction,
                                            fields=non_side_effect_fields,
                                            data=data)
    return transaction


def transaction_delete(user_id: int, transaction_id: int):
    user = get_object(User, id=user_id)
    transaction = get_object(Transaction, id=transaction_id, account__user=user)

    transaction.delete()
