import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene import Node


from .models import *
from .schema_inputs import *


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


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)
    error = graphene.String()

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            user_instance = User()
            if user_instance and input:
                for key, value in input.items():
                    if key == "password":
                        user_instance.set_password(value)
                    else:
                        setattr(user_instance, key, value)
                user_instance.save()
                ok = True
                return CreateUser(ok=ok, user=user_instance)
            else:
                return CreateUser(
                    ok=ok,
                    user=None,
                    error="User instance cannot be created\\n or input empty",
                )
        except Exception as ex:
            return CreateUser(ok=ok, user=None, error=str(ex))


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=False)
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserNode)
    error = graphene.String()

    @staticmethod
    def mutate(root, info, id=None, input=None):
        ok = False
        try:
            user_instance = User.objects.get(pk=id)
            if input:
                for key, value in input.items():
                    if key == "password":
                        user_instance.set_password(value)
                    else:
                        setattr(user_instance, key, value)
                user_instance.save()
                ok = True
                return UpdateUser(ok=ok, user=user_instance)
            else:
                return UpdateUser(
                    ok=ok,
                    user=None,
                    error="User instance cannot be created or input empty",
                )
        except Exception as ex:
            return UpdateUser(ok=ok, user=None, error=str(ex))


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=False)
        input = UserInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

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
            return DeleteUser(ok=ok, error=None)
        except Exception as ex:
            return DeleteUser(ok=ok, error=str(ex))


class CreateCustomerOrder(graphene.Mutation):
    class Arguments:
        input = CustomerOrderInput(required=True)

    ok = graphene.Boolean()
    customer_order = graphene.Field(CustomerOrderNode)
    error = graphene.String()

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            customer_order_instance = CustomerOrder()
            if customer_order_instance and input:
                user_instance = User.objects.get(pk=input.id_user_id.id)
                animal_instance = Livestock.objects.get(pk=input.id_animal_id.id_animal)
                for key, value in input.items():
                    if key != "id_user_id" and key != "id_animal_id":
                        setattr(customer_order_instance, key, value)
                setattr(customer_order_instance, "id_user_id", user_instance.id)
                setattr(
                    customer_order_instance, "id_animal_id", animal_instance.id_animal
                )
                customer_order_instance.save()
                ok = True
                return CreateCustomerOrder(
                    ok=ok, customer_order=customer_order_instance, error=None
                )
            else:
                return CreateCustomerOrder(
                    ok=ok, customer_order=None, error="user or input empty",
                )
        except Exception as ex:
            return CreateCustomerOrder(ok=ok, customer_order=None, error=str(ex))


class UpdateCustomerOrder(graphene.Mutation):
    class Arguments:
        input = CustomerOrderInput(required=True)

    ok = graphene.Boolean()
    customer_order = graphene.Field(CustomerOrderNode)
    error = graphene.String()

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            if input:
                id_order = input.id_order
                customer_order_instance = CustomerOrder.objects.get(pk=id_order)
                for key, value in input.items():
                    setattr(customer_order_instance, key, value)
                customer_order_instance.save()
                ok = True
                return UpdateCustomerOrder(
                    ok=ok, customer_order=customer_order_instance, error=None
                )
        except Exception as ex:
            print(ex)
            return UpdateCustomerOrder(ok=ok, customer_order=None)


class DeleteCustomerOrder(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=False)
        input = CustomerOrderInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    def mutate(root, info, pk=None, input=None):
        ok = False
        try:
            if "id_order" in input:
                customer_order_instance = CustomerOrder.objects.get(pk=input.id_order)
            else:
                customer_order_instance = CustomerOrder.objects.get(pk=pk)
            customer_order_instance.delete()
            ok = True
            return DeleteCustomerOrder(ok=ok, error=None)
        except Exception as ex:
            return DeleteCustomerOrder(ok=ok, error=str(ex))


class CreateFarmOrder(graphene.Mutation):
    class Arguments:
        input = FarmOrderInput(required=True)

    ok = graphene.Boolean()
    farm_order = graphene.Field(FarmOrderNode)
    error = graphene.String()

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            farm_order_instance = FarmOrder()
            if farm_order_instance and input:
                user_instance = User.objects.get(pk=input.id_user_id.id)
                animal_instance = Livestock.objects.get(pk=input.id_animal_id.id_animal)
                for key, value in input.items():
                    if key != "id_user_id" and key != "id_animal_id":
                        setattr(farm_order_instance, key, value)
                setattr(farm_order_instance, "id_user_id", user_instance.id)
                setattr(farm_order_instance, "id_animal_id", animal_instance.id_animal)
                farm_order_instance.save()
                ok = True
                return CreateFarmOrder(
                    ok=ok, farm_order=farm_order_instance, error=None
                )
            else:
                return CreateFarmOrder(
                    ok=ok, farm_order=None, error="farm order obj error or input empty"
                )
        except Exception as ex:
            return CreateFarmOrder(ok=ok, farm_order=None, error=str(ex))


class UpdateFarmOrder(graphene.Mutation):
    class Arguments:
        input = FarmOrderInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()
    farm_order = graphene.Field(FarmOrderNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            if input:
                id_order = input.id_order
                farm_order_instance = FarmOrder.objects.get(pk=id_order)
                for key, value in input.items():
                    setattr(farm_order_instance, key, value)
                farm_order_instance.save()
                ok = True
                return UpdateFarmOrder(
                    ok=ok, farm_order=farm_order_instance, error=None
                )
            else:
                return UpdateFarmOrder(ok=ok, farm_order=None, error="input empty")
        except Exception as ex:
            return UpdateFarmOrder(ok=ok, farm_order=None, error=str(ex))


class DeleteFarmOrder(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=False)
        input = FarmOrderInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    def mutate(root, info, pk=None, input=None):
        ok = False
        try:
            if "id_order" in input:
                farm_order_instance = FarmOrder.objects.get(pk=input.id_order)
            else:
                farm_order_instance = FarmOrder.objects.get(pk=pk)
            farm_order_instance.delete()
            ok = True
            return DeleteFarmOrder(ok=ok, error=None)
        except Exception as ex:
            return DeleteFarmOrder(ok=ok, error=str(ex))


class CreateMiddlemanOrder(graphene.Mutation):
    class Arguments:
        input = MiddlemanOrderInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()
    middleman_order = graphene.Field(MiddlemanOrderNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            middleman_order_instance = MiddlemanOrder()
            if middleman_order_instance and input:
                user_instance = User.objects.get(pk=input.id_user_id.id)
                animal_instance = Livestock.objects.get(pk=input.id_animal_id.id_animal)
                for key, value in input.items():
                    if key != "id_user_id" and key != "id_animal_id":
                        setattr(middleman_order_instance, key, value)
                setattr(middleman_order_instance, "id_user_id", user_instance.id)
                setattr(
                    middleman_order_instance, "id_animal_id", animal_instance.id_animal
                )
                middleman_order_instance.save()
                ok = True
                return CreateMiddlemanOrder(
                    ok=ok, middleman_order=middleman_order_instance, error=None
                )
            else:
                return CreateMiddlemanOrder(
                    ok=ok, middleman_order=None, error="Input empty or order obj error"
                )
        except Exception as ex:
            return CreateMiddlemanOrder(ok=ok, middleman_order=None, error=str(ex))


class UpdateMiddlemanOrder(graphene.Mutation):
    class Arguments:
        input = MiddlemanOrderInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()
    middleman_order = graphene.Field(MiddlemanOrderNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            if input:
                id_order = input.id_order
                middleman_order_instance = MiddlemanOrder.objects.get(pk=id_order)
                for key, value in input.items():
                    setattr(middleman_order_instance, key, value)
                middleman_order_instance.save()
                ok = True
                return UpdateMiddlemanOrder(
                    ok=ok, middleman_order=middleman_order_instance, error=None
                )
            else:
                return UpdateMiddlemanOrder(
                    ok=ok, middleman_order=None, error="Input empty"
                )
        except Exception as ex:
            return UpdateMiddlemanOrder(ok=ok, middleman_order=None, error=str(ex))


class DeleteMiddlemanOrder(graphene.Mutation):
    class Arguments:
        pk = graphene.ID(required=False)
        input = MiddlemanOrderInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    def mutate(root, info, pk=None, input=None):
        ok = False
        try:
            if "id_order" in input:
                middleman_order_instance = MiddlemanOrder.objects.get(pk=input.id_order)
            else:
                middleman_order_instance = MiddlemanOrder.objects.get(pk=pk)
            middleman_order_instance.delete()
            ok = True
            return DeleteMiddlemanOrder(ok=ok, error=None)
        except Exception as ex:
            return DeleteMiddlemanOrder(ok=ok, error=str(ex))


class CreateFarm(graphene.Mutation):
    class Arguments:
        input = FarmInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()
    farm = graphene.Field(FarmNode)

    @staticmethod
    def mutate(root, info, input):
        ok = False
        try:
            farm_instance = Farm()
            if farm_instance and input:
                user_instance = User.objects.get(pk=input.id_user_id.id)
                for key, value in input.items():
                    if key != "id_user_id":
                        setattr(farm_instance, key, value)
                setattr(farm_instance, "id_user_id", user_instance.id)
                farm_instance.save()
                ok = True
                return CreateFarm(ok=ok, farm=farm_instance, error=None)
            else:
                return CreateFarm(
                    ok=ok, farm=None, error="Input empty or farm obj error"
                )
        except Exception as ex:
            return CreateFarm(ok=ok, error=str(ex), farm=None)


class UpdateFarm(graphene.Mutation):
    class Arguments:
        input = FarmInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()
    farm = graphene.Field(FarmNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            if "id_farm" in input:
                id_farm = input.id
                farm_instance = Farm.objects.get(pk=id_farm)
                if farm_instance and input:
                    for key, value in input.items():
                        setattr(farm_instance, key, value)
                    farm_instance.save()
                    ok = True
                    return UpdateFarm(ok=ok, farm=farm_instance, error=None)
            else:
                return UpdateFarm(ok=ok, farm=None, error="Farm object not found by PK")
        except Exception as ex:
            return UpdateFarm(ok=ok, error=str(ex), farm=None)


class DeleteFarm(graphene.Mutation):
    class Arguments:
        input = FarmInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            if "id_farm" in input:
                farm_instance = Farm.objects.get(pk=input.id_farm)
                farm_instance.delete()
                ok = True
                return DeleteFarm(ok=ok, error=None)
            else:
                return DeleteFarm(ok=ok, error="PK not found in inputs")
        except Exception as ex:
            return DeleteFarm(ok=ok, error=str(ex))


class CreateLivestock(graphene.Mutation):
    class Arguments:
        input = LivestockInput(required=True)

    ok = graphene.Boolean()
    livestock = graphene.Field(LivestockNode)
    error = graphene.String()

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            livestock_instance = Livestock()
            if livestock_instance and input:
                id_farm = input.id_farm_id.id_farm
                farm_instance = Farm.objects.get(pk=id_farm)
                for key, value in input.items():
                    if key != "id_farm_id":
                        setattr(livestock_instance, key, value)
                setattr(livestock_instance, "id_farm_id", farm_instance.id_farm)
                livestock_instance.save()
                ok = True
                return CreateLivestock(ok=ok, livestock=livestock_instance, error=None)
            else:
                return CreateLivestock(
                    ok=ok, livestock=None, error="Input empty or livestock obj error"
                )
        except Exception as ex:
            return CreateLivestock(ok=ok, error=str(ex), livestock=None)


class UpdateLivestock(graphene.Mutation):
    class Arguments:
        input = LivestockInput(required=True)

    ok = graphene.Boolean()
    livestock = graphene.Field(LivestockNode)
    error = graphene.String()

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            id_animal = input.id_animal
            livestock_instance = Livestock.objects.get(pk=id_animal)
            if livestock_instance and input:
                for key, value in input.items():
                    setattr(livestock_instance, key, value)
                livestock_instance.save()
                ok = True
                return UpdateLivestock(ok=ok, livestock=livestock_instance, error=None)
            else:
                return UpdateLivestock(
                    ok=ok, livestock=None, error="input empty or livestock pk not found"
                )
        except Exception as ex:
            return UpdateLivestock(ok=ok, error=str(ex), livestock=None)


class DeleteLivestock(graphene.Mutation):
    class Arguments:
        input = LivestockInput(required=True)

    ok = graphene.Boolean()
    error = graphene.String()

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            if "id_animal" in input:
                livestock_instance = Livestock.objects.get(pk=input.id_animal)
                livestock_instance.delete()
                ok = True
                return DeleteFarm(ok=ok, error=None)
            else:
                return DeleteFarm(ok=ok, error="PK not found in inputs")
        except Exception as ex:
            return DeleteFarm(ok=ok, error=str(ex))


class Query(graphene.ObjectType):

    farm = Node.Field(FarmNode)
    users = Node.Field(UserNode)
    animal = Node.Field(LivestockNode)
    farm_order = Node.Field(FarmOrderNode)
    customer_order = Node.Field(CustomerOrderNode)
    middleman_order = Node.Field(MiddlemanOrderNode)
    all_users = DjangoFilterConnectionField(UserNode)
    all_farms = DjangoFilterConnectionField(FarmNode)
    all_animals = DjangoFilterConnectionField(LivestockNode)
    all_farm_orders = DjangoFilterConnectionField(FarmOrderNode)
    all_customer_orders = DjangoFilterConnectionField(CustomerOrderNode)
    all_middleman_orders = DjangoFilterConnectionField(MiddlemanOrderNode)


class Mutation(graphene.ObjectType):

    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_farm = CreateFarm.Field()
    update_farm = UpdateFarm.Field()
    delete_farm = DeleteFarm.Field()
    create_livestock = CreateLivestock.Field()
    update_livestock = UpdateLivestock.Field()
    delete_livestock = DeleteLivestock.Field()
    create_farm_order = CreateFarmOrder.Field()
    update_farm_order = UpdateFarmOrder.Field()
    delete_farm_order = DeleteFarmOrder.Field()
    create_customer_order = CreateCustomerOrder.Field()
    update_customer_order = UpdateCustomerOrder.Field()
    delete_customer_order = DeleteCustomerOrder.Field()
    create_middleman_order = CreateMiddlemanOrder.Field()
    update_middleman_order = UpdateMiddlemanOrder.Field()
    delete_middleman_order = DeleteMiddlemanOrder.Field()
