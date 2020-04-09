import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graphene import Schema, relay, resolve_only_args
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Node

from .models import User, Farm, Livestock, FarmOrder, MiddlemanOrder, CustomerOrder


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)
        filter_fields = {
            "id": ["exact", "icontains", "istartswith"],
            "email": ["exact", "icontains", "istartswith"],
            "username": ["exact", "icontains", "istartswith"],
            "user_type": ["exact", "icontains", "istartswith"],
            # "date_joined": []
        }


class FarmNode(DjangoObjectType):
    class Meta:
        model = Farm
        interfaces = (Node,)
        filter_fields = {
            "id_farm": ["exact", "icontains", "istartswith"],
            "n_cow": ["exact", "gte", "lte", "gt", "lt", "range"],
            "n_bull": ["exact", "gte", "lte", "gt", "lt", "range"],
            "n_calf": ["exact", "gte", "lte", "gt", "lt", "range"],
            "id_user__id": ["exact"],
            "id_user__email": ["exact"],
        }


class LivestockNode(DjangoObjectType):
    class Meta:
        model = Livestock
        interfaces = (Node,)
        filter_fields = {
            "chapeta": ["exact", "icontains", "istartswith"],
            "price": ["exact", "gte", "lte", "gt", "lt", "range"],
            "weight": ["exact", "gte", "lte", "gt", "lt", "range"],
            "raze": ["exact", "icontains", "istartswith"],
            "status": ["exact"],
            "id_farm__id_user": ["exact"],
        }


class FarmOrderNode(DjangoObjectType):
    class Meta:
        model = FarmOrder
        interfaces = (Node,)
        filter_fields = {
            "id_order": ["exact", "icontains", "istartswith"],
            "status": ["exact", "icontains", "istartswith"],
            "id_user__id": ["exact"],
            "id_user__user_type": ["icontains", "istartswith"],
            "id_user__email": ["exact"],
            "id_animal__id_animal": ["exact"],
        }


class MiddlemanOrderNode(DjangoObjectType):
    class Meta:
        model = MiddlemanOrder
        interfaces = (Node,)
        filter_fields = {
            "id_order": ["exact", "icontains", "istartswith"],
            "status": ["exact", "icontains", "istartswith"],
            "id_user__user_type": ["icontains", "istartswith"],
            "id_user__id": ["exact"],
            "id_user__email": ["exact"],
            "id_animal__id_animal": ["exact"],
        }


class CustomerOrderNode(DjangoObjectType):
    class Meta:
        model = CustomerOrder
        interfaces = (Node,)
        filter_fields = {
            "id_order": ["exact", "icontains", "istartswith"],
            "status": ["exact", "icontains", "istartswith"],
            "id_user__user_type": ["icontains", "istartswith"],
            "id_user__id": ["exact"],
            "id_user__email": ["exact"],
            "id_animal__id_animal": ["exact"],
        }


class UserInput(graphene.InputObjectType):
    nit = graphene.String(required=False)
    email = graphene.String(required=False)
    username = graphene.String(required=False)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    user_type = graphene.String(required=False)
    phone = graphene.String(required=False)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user_instance = User.objects.get(pk=id)
        if user_instance and input:

            ok = True
            for k, v in input.items():
                setattr(user_instance, k, v)
            user_instance.save()
            return UpdateUser(ok=ok, user=user_instance)
        return UpdateUser(ok=ok, user=None)


class Query(graphene.ObjectType):
    animal = Node.Field(LivestockNode)
    all_animals = DjangoFilterConnectionField(LivestockNode)
    middlemanorder = Node.Field(MiddlemanOrderNode)
    all_middlemanorders = DjangoFilterConnectionField(MiddlemanOrderNode)
    customerorder = Node.Field(CustomerOrderNode)
    all_customerorders = DjangoFilterConnectionField(CustomerOrderNode)
    # users = Node.Field(UserNode)
    # all_users = DjangoFilterConnectionField(UserNode)
    farmorder = Node.Field(FarmOrderNode)
    all_farmorder = DjangoFilterConnectionField(FarmOrderNode)
    farm = Node.Field(FarmNode)
    all_farm = DjangoFilterConnectionField(FarmNode)


class Mutation(graphene.ObjectType):
    # create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
