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
    id = graphene.ID(required=False)
    nit = graphene.String(required=False)
    email = graphene.String(required=False)
    username = graphene.String(required=False)
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)
    user_type = graphene.String(required=False)
    phone = graphene.String(required=False)
    password = graphene.String(required=False)


class LivestockInput(graphene.InputObjectType):
    id_animal = graphene.ID()


class FarmOrderInput(graphene.InputObjectType):
    id_animal_id = graphene.Field(LivestockInput)
    id_user_id = graphene.Field(UserInput)
    status = graphene.String(required=False)
    detail = graphene.String(required=False)


class MiddlemanOrderInput(graphene.InputObjectType):
    id_animal_id = graphene.Field(LivestockInput)
    id_user_id = graphene.Field(UserInput)
    status = graphene.String(required=False)
    detail = graphene.String(required=False)


class CustomerOrderInput(graphene.InputObjectType):
    id_user_id = graphene.Field(UserInput)
    id_animal_id = graphene.Field(LivestockInput)
    status = graphene.String(required=False)
    details = graphene.String(required=False)


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            user_instance = User()
            farm_order = FarmOrder()
            if user_instance and input:
                for k, v in input.items():
                    if k == "password":
                        user_instance.set_password(v)
                    else:
                        setattr(user_instance, k, v)
                user_instance.save()
                ok = True
                return CreateUser(ok=ok, user=user_instance)
        except:
            return CreateUser(ok=ok, user=None)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=False)
        input = UserInput(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id=None, input=None):
        ok = False
        try:
            if "email" in input:
                user_instance = User.objects.get(email=input.email)
            else:
                user_instance = User.objects.get(pk=id)
            user_instance.delete()
            ok = True
            return DeleteUser(ok=ok)
        except:
            return DeleteUser(ok=ok)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        try:
            user_instance = User.objects.get(pk=id)
            if user_instance and input:
                for k, v in input.items():
                    if k == "password":
                        user_instance.set_password(v)
                    else:
                        setattr(user_instance, k, v)
                user_instance.save()
                ok = True
                return UpdateUser(ok=ok, user=user_instance)
        except:
            return UpdateUser(ok=ok, user=None)


# class CreateCustomerOrder(graphene.Mutation):
#     class Arguments:
#         input = CustomerOrderInput(required=True)
#
#     ok = graphene.Boolean()
#     customer_order = graphene.Field(CustomerOrderNode)
#
#     @staticmethod
#     def mutate(root, info, input=None):
#         ok = False
#         try:
#             customer_order_instance = CustomerOrder()
#             if customer_order_instance and input:
#                 for k, v in input.items():
#                     if input
#                     setattr(customer_order_instance, k, v)
#                 customer_order_instance.save()
#                 ok = True
#                 return CreateCustomerOrder(
#                     ok=ok, customer_order=customer_order_instance
#                 )
#         except:
#             return CreateCustomerOrder(ok=ok, customer_order=None)


class CreateFarmOrder(graphene.Mutation):
    class Arguments:
        input = FarmOrderInput(required=True)

    ok = graphene.Boolean()
    farm_order = graphene.Field(FarmOrderNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            farm_order_instance = FarmOrder()
            user_instance = User.objects.get(pk=input.id_user_id.id)
            animal_instance = Livestock.objects.get(pk=input.id_animal_id.id_animal)
            if farm_order_instance and input:
                for k, v in input.items():
                    if k != "id_user_id" and k != "id_animal_id":
                        setattr(farm_order_instance, k, v)
                setattr(farm_order_instance, "id_user_id", user_instance.id)
                setattr(farm_order_instance, "id_animal_id", animal_instance.id_animal)
                farm_order_instance.save()
                ok = True
                return CreateFarmOrder(ok=ok, farm_order=farm_order_instance)
        except:
            return CreateFarmOrder(ok=ok, farm_order=None)


# class DeleteFarmOrderNode(graphene.Mutation):
#     pass


# class UpdateFarmOrder(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID()
#         input = FarmOrderInput(required=True)
#
#     ok = graphene.Boolean()
#     update_user = graphene.Field(UserNode)
#
#     @staticmethod
#     def mutate(root, info, id, input=None):
#         ok = False
#         try:
#             user_instance = FarmOrder.objects.get(pk=id)
#             if user_instance and input:
#                 for k, v in input.items():
#                     setattr(user_instance, k, v)
#                 user_instance.save()
#                 ok = True
#                 return UpdateFarmOrder(ok=ok, update_user=user_instance)
#         except:
#             return UpdateFarmOrder(ok=ok, update_user=None)


# class CreateMiddlemanOrder(graphene.Mutation):
#     class Arguments:
#         input = MiddlemanOrderInput(required=True)
#
#     ok = graphene.Boolean()
#     farm_order = graphene.Field(MiddlemanOrderNode)
#
#     @staticmethod
#     def mutate(root, info, input=None):
#         ok = False
#         try:
#             farm_order_instance = FarmOrder()
#             user_instance = User.objects.get(pk=input.id_user.id)
#             animal_instance = Livestock.objects.get(pk=input.id_animal.id_animal)
#             if farm_order_instance and input:
#                 for k, v in input.items():
#                     if k != "id_user" and k != "id_animal":
#                         setattr(farm_order_instance, k, v)
#                 farm_order_instance.id_user.set(user_instance)
#                 farm_order_instance.id_animal.set(animal_instance)
#                 farm_order_instance.save()
#                 ok = True
#                 return CreateFarmOrder(ok=ok, farm_order=farm_order_instance)
#         except:
#             return CreateFarmOrder(ok=ok, farm_order=None)


# class DeleteFarmOrderNode(graphene.Mutation):
#     pass


class UpdateMiddlemanOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        input = MiddlemanOrderInput(required=True)

    ok = graphene.Boolean()
    update_user = graphene.Field(UserNode)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        try:
            user_instance = MiddlemanOrder.objects.get(pk=id)
            if user_instance and input:
                for k, v in input.items():
                    setattr(user_instance, k, v)
                user_instance.save()
                ok = True
                return UpdateMiddlemanOrder(ok=ok, update_user=user_instance)
        except:
            return UpdateMiddlemanOrder(ok=ok, update_user=None)


class Query(graphene.ObjectType):
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
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    create_farm_order = CreateFarmOrder.Field()
    # update_farm_order = UpdateFarmOrder.Field()
    # create_MiddlemanOrder = CreateMiddlemanOrder.Field()
    # update_MiddlemanOrder = UpdateMiddlemanOrder.Field()
    delete_user = DeleteUser.Field()
