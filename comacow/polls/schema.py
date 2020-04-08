import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Node

from .models import User, Farm, Livestock, FarmOrder, MiddlemanOrder, CustomerOrder


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        # interfaces = (Node,)
        # filter_fields = {}


class FarmNode(DjangoObjectType):
    class Meta:
        model = Farm


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


class MiddlemanOrderNode(DjangoObjectType):
    class Meta:
        model = MiddlemanOrder
        interfaces = (Node,)
        filter_fields = {
            "id_order": ["exact", "icontains", "istartswith"],
            "status": ["exact", "icontains", "istartswith"],
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
