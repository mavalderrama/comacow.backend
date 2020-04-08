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


class UserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        nit = graphene.String(required=True)
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        user_type = graphene.String(required=True)
        phone = graphene.String(required=False)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserNode)

    def mutate(
        self, info, id, nit, email, username, first_name, last_name, user_type, phone
    ):
        user = User.objects.get(pk=id)
        user.nit = nit
        user.email = email
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.user_type = user_type
        user.phone = phone
        user.save()
        # Notice we return an instance of this mutation
        return UserMutation(user=user)


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


class Mutation(graphene.ObjectType):
    update_user = UserMutation.Field()
