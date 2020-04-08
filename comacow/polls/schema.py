import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Node

from .models import User, Farm, Livestock, FarmOrder, MiddlemanOrder, CustomerOrder


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node,)
        filter_fields = {
            "id": ["exact", "gte", "lte", "gt", "lt", "range"],
            "email": ["exact", "icontains", "istartswith"],
            "username": ["exact", "icontains", "istartswith"],
            "user_type": ["exact", "icontains", "istartswith"],
            #"date_joined": []
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
            "id_user__user_type": ["icontains","istartswith"],
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


class Query(ObjectType):
    animal = Node.Field(LivestockNode)
    all_animals = DjangoFilterConnectionField(LivestockNode)
    middlemanorder = Node.Field(MiddlemanOrderNode)
    all_middlemanorders = DjangoFilterConnectionField(MiddlemanOrderNode)
    customerorder = Node.Field(CustomerOrderNode)
    all_customerorders = DjangoFilterConnectionField(CustomerOrderNode)
    users = Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)
    farmorder = Node.Field(FarmOrderNode)
    all_farmorder = DjangoFilterConnectionField(FarmOrderNode)
    farm = Node.Field(FarmNode)
    all_farm = DjangoFilterConnectionField(FarmNode)


# class UserInput(graphene.InputObjectType):
#     nit = graphene.String()
#     email = graphene.String()
#     username = graphene.String()
#     first_name = graphene.String()
#     last_name = graphene.String()
#     user_type = graphene.String()
#     phone = graphene.String()
#     is_active = graphene.Boolean()


# class CreateUser(graphene.Mutation):
#     class Arguments:
#         input = UserInput(required=True)
#
#     ok = graphene.Boolean()
#     user = graphene.Field(UserType)
#
#     @staticmethod
#     def mutate(root, info, input=None):
#         ok = True
#         actor_instance = User(name=input.name)
#         actor_instance.save()
#         return CreateUser(ok=ok, actor=actor_instance)
