from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Account, Transaction
from .selectors import account_list, transaction_list
from .serializers import AccountSerializer

from .services import (account_create,
                       account_update,
                       account_delete,
                       transaction_create,
                       transaction_update,
                       transaction_delete)
from flowback.common.pagination import LimitOffsetPagination, get_paginated_response


class AccountListAPI(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 20
        max_limit = 100

    class FilterSerializer(serializers.Serializer):
        order_by = serializers.CharField(required=False)
        id = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        account_number = serializers.CharField()
        account_name = serializers.CharField()
        balance = serializers.FloatField()

    def get(self, request):
        serializer = self.FilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        accounts = account_list(user=request.user)

        return get_paginated_response(pagination_class=self.Pagination,
                                      serializer_class=self.OutputSerializer,
                                      queryset=accounts,
                                      request=request,
                                      view=self)


class AccountCreateAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Account
            fields = ['id', 'account_number', 'account_name']

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = account_create(user_id=request.user.id,
                                 **serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data=account.id)


class AccountUpdateApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Account
            fields = ['id', 'account_number', 'account_name']

    def post(self, request, account_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account_update(user_id=request.user.id, account_id=account_id,
                       data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class AccountDeleteAPI(APIView):
    def post(self, request, account_id: int):
        account_delete(user_id=request.user.id, account_id=account_id)

        return Response(status=status.HTTP_200_OK)


class TransactionListAPI(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 20
        max_limit = 100

    class FilterSerializer(serializers.Serializer):
        account_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
        order_by = serializers.CharField(required=False)
        id = serializers.IntegerField(required=False)
        date_after = serializers.DateField(required=False)
        date_before = serializers.DateField(required=False)
        description = serializers.CharField(required=False)
        accounts = serializers.CharField(required=False)

    class OutputSerializer(serializers.Serializer):
        account = AccountSerializer()
        id = serializers.IntegerField()
        debit_amount = serializers.FloatField()
        credit_amount = serializers.FloatField()
        description = serializers.CharField()
        verification_number = serializers.CharField()
        date = serializers.DateTimeField()

    def get(self, request):
        serializer = self.FilterSerializer(data=request.query_params)
        print("GEEEET", serializer)
        serializer.is_valid(raise_exception=True)

        account_ids = serializer.validated_data.get('account_ids', [])

        # if account_ids:
        #     filters['account_ids'] = account_ids

        # transactions = transaction_list(filters=serializer.validated_data, user=request.user)
        transactions = Transaction.objects.all()
        if account_ids:
            transactions = transactions.filter(account_id__in=account_ids)
        print(account_ids)

        return get_paginated_response(pagination_class=self.Pagination,
                                      serializer_class=self.OutputSerializer,
                                      queryset=transactions,
                                      request=request,
                                      view=self)


class TransactionCreateAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            fields = ['id', 'debit_amount', 'credit_amount',
                      'description', 'verification_number', 'date']

        def validate(self, data):
            if not data.get('debit_amount') and not data.get('credit_amount'):
                raise serializers.ValidationError(
                    "You must provide a debit or credit amount.")
            if data.get('debit_amount') and data.get('credit_amount'):
                raise serializers.ValidationError(
                    "Each transaction must have either a debit or a credit amount, but not both")
            if data.get('debit_amount', 0) <= 0 and data.get('credit_amount', 0) <= 0:
                raise serializers.ValidationError(
                    "The debit or credit amount must be greater than zero.")
            return data

    def post(self, request, account_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = transaction_create(account_id=account_id, user_id=request.user.id,
                                     **serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data=account.id)


class TransactionUpdateApi(APIView):
    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Transaction
            fields = ['id', 'debit_amount', 'credit_amount',
                      'description', 'verification_number', 'date']

        def validate(self, data):
            if not data.get('debit_amount') and not data.get('credit_amount'):
                raise serializers.ValidationError(
                    "You must provide a debit or credit amount.")
            if data.get('debit_amount') and data.get('credit_amount'):
                raise serializers.ValidationError(
                    "Each transaction must have either a debit or a credit amount, but not both")
            if data.get('debit_amount', 0) <= 0 and data.get('credit_amount', 0) <= 0:
                raise serializers.ValidationError(
                    "The debit or credit amount must be greater than zero.")
            return data

    def post(self, request, account_id: int, transaction_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        transaction_update(user_id=request.user.id,
                           transaction_id=transaction_id,
                           data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK)


class TransactionDeleteAPI(APIView):
    def post(self, request, account_id: int, transaction_id: int):
        transaction_delete(user_id=request.user.id,
                           transaction_id=transaction_id)

        return Response(status=status.HTTP_200_OK)
