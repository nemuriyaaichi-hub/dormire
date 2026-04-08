from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    CharField,
    CurrentUserDefault,
    HiddenField,
    ModelSerializer,
    UUIDField,
    ValidationError,
)

from recommends.models import PillowRec

from .models import Customer, MatOrder, MatRec, Order, PillowOrder


class PillowOrderSerializer(ModelSerializer):
    recommend_pillow = UUIDField(source="pillow_rec")

    class Meta:
        model = PillowOrder
        fields = (
            "id",
            "recommend_pillow",
            "material",
            "cover_material",
            "cover_color1",
            "cover_color2",
            "cover_color3",
        )


class MatOrderSerializer(ModelSerializer):
    recommend_mattress1 = UUIDField(source="mat_rec1")
    recommend_mattress2 = UUIDField(source="mat_rec2", allow_null=True)

    class Meta:
        model = MatOrder
        fields = (
            "id",
            "recommend_mattress1",
            "recommend_mattress2",
            "size",
            "thickness",
            "cover_material",
            "cover_color1",
            "cover_color2",
            "cover_color3",
        )


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        exclude = (
            "id",
            "created_at",
            "updated_at",
        )


class OrderSerializer(ModelSerializer):
    customer = CustomerSerializer(write_only=True)
    mattress = MatOrderSerializer(
        source="mat_order",
        allow_null=True,
        write_only=True,
        required=False,
    )
    pillow1 = PillowOrderSerializer(
        source="pillow_order1",
        allow_null=True,
        write_only=True,
        required=False,
    )
    pillow2 = PillowOrderSerializer(
        source="pillow_order2",
        allow_null=True,
        write_only=True,
        required=False,
    )
    user = HiddenField(default=CurrentUserDefault())
    status = CharField(default="OK", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "customer",
            "pillow1",
            "pillow2",
            "mattress",
            "status",
        )
        read_only_fields = (
            "id",
            "status",
        )

    @transaction.atomic
    def create(self, validated_data):
        customer_data = validated_data.pop("customer")
        customer = Customer.objects.create(**customer_data)
        order = Order.objects.create(
            customer=customer,
            user=validated_data.pop("user"),
        )
        pillow1_data = validated_data.pop("pillow_order1", None)
        if pillow1_data:
            pillow1_rec_id = pillow1_data.pop("pillow_rec", None)
            pillow1_rec = get_object_or_404(PillowRec, id=pillow1_rec_id)
            pillow1 = PillowOrder.objects.create(pillow_rec=pillow1_rec, **pillow1_data)
            order.pillow_order1 = pillow1
            order.hearing1 = pillow1_rec.hearing

        pillow2_data = validated_data.pop("pillow_order2", None)
        if pillow2_data:
            pillow2_rec_id = pillow2_data.pop("pillow_rec", None)
            pillow2_rec = get_object_or_404(PillowRec, id=pillow2_rec_id)
            pillow2 = PillowOrder.objects.create(pillow_rec=pillow2_rec, **pillow2_data)
            order.pillow_order2 = pillow2
            order.hearing2 = pillow2_rec.hearing

        mat_order_data = validated_data.pop("mat_order", None)
        if mat_order_data:
            mat_rec1_id = mat_order_data.pop("mat_rec1", None)
            mat_rec1 = get_object_or_404(MatRec, id=mat_rec1_id)
            mat_rec2_id = mat_order_data.pop("mat_rec2", None)
            if mat_rec2_id:
                mat_rec2 = get_object_or_404(MatRec, id=mat_rec2_id)
            else:
                mat_rec2 = None
            mat_order = MatOrder.objects.create(
                mat_rec1=mat_rec1, mat_rec2=mat_rec2, **mat_order_data
            )
            order.mat_order = mat_order

            if order.hearing1 and order.hearing1 != mat_rec1.hearing:
                raise ValidationError(
                    {"non_fields_errors": "1人目の枕とマットレスのヒアリング情報が一致しません。"}
                )
            else:
                order.hearing1 = mat_rec1.hearing

            if mat_rec2_id:
                if order.hearing2 and order.hearing2 != mat_rec2.hearing:
                    raise ValidationError(
                        {"non_fields_errors": "2人目の枕とマットレスのヒアリング情報が一致しません。"}
                    )
                else:
                    order.hearing2 = mat_rec2.hearing

        order.save()
        return order
