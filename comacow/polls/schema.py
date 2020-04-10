import graphene
from graphene_django.types import DjangoObjectType
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
    id_order = graphene.ID()
    id_animal_id = graphene.Field(LivestockInput)
    id_user_id = graphene.Field(UserInput)
    status = graphene.String(required=False)
    details = graphene.String(required=False)


class MiddlemanOrderInput(graphene.InputObjectType):
    id_order = graphene.ID()
    id_animal_id = graphene.Field(LivestockInput)
    id_user_id = graphene.Field(UserInput)
    status = graphene.String(required=False)
    details = graphene.String(required=False)


class CustomerOrderInput(graphene.InputObjectType):
    id_order = graphene.ID()
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
                for key, value in input.items():
                    if key == "password":
                        user_instance.set_password(value)
                    else:
                        setattr(user_instance, key, value)
                user_instance.save()
                ok = True
                return UpdateUser(ok=ok, user=user_instance)
        except:
            return UpdateUser(ok=ok, user=None)


class CreateCustomerOrder(graphene.Mutation):
    class Arguments:
        input = CustomerOrderInput(required=True)

    ok = graphene.Boolean()
    customer_order = graphene.Field(CustomerOrderNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            customer_order_instance = CustomerOrder()
            user_instance = User.objects.get(pk=input.id_user_id.id)
            animal_instance = Livestock.objects.get(pk=input.id_animal_id.id_animal)
            if customer_order_instance and input:
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
                    ok=ok, customer_order=customer_order_instance
                )
        except:
            return CreateCustomerOrder(ok=ok, customer_order=None)


class UpdateCustomerOrder(graphene.Mutation):
    class Arguments:
        input = CustomerOrderInput(required=True)

    ok = graphene.Boolean()
    customer_order = graphene.Field(CustomerOrderNode)

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            id_order = input.id_order
            customer_order_instance = CustomerOrder.objects.get(pk=id_order)
            if customer_order_instance and input:
                for key, value in input.items():
                    setattr(customer_order_instance, key, value)
                customer_order_instance.save()
                ok = True
                return UpdateCustomerOrder(
                    ok=ok, customer_order=customer_order_instance
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

    @staticmethod
    def mutate(root, info, input=None):
        ok = False
        try:
            farm_order_instance = FarmOrder()
            user_instance = User.objects.get(pk=input.id_user_id.id)
            animal_instance = Livestock.objects.get(pk=input.id_animal_id.id_animal)
            if farm_order_instance and input:
                for key, value in input.items():
                    if key != "id_user_id" and key != "id_animal_id":
                        setattr(farm_order_instance, key, value)
                setattr(farm_order_instance, "id_user_id", user_instance.id)
                setattr(farm_order_instance, "id_animal_id", animal_instance.id_animal)
                farm_order_instance.save()
                ok = True
                return CreateFarmOrder(ok=ok, farm_order=farm_order_instance)
        except:
            return CreateFarmOrder(ok=ok, farm_order=None)


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
            id_order = input.id_order
            farm_order_instance = FarmOrder.objects.get(pk=id_order)
            if farm_order_instance and input:
                for key, value in input.items():
                    setattr(farm_order_instance, key, value)
                farm_order_instance.save()
                ok = True
                return UpdateFarmOrder(
                    ok=ok, farm_order=farm_order_instance, error=None
                )
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
            return DeleteFarmOrder(ok=ok, error="")
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
            user_instance = User.objects.get(pk=input.id_user_id.id)
            animal_instance = Livestock.objects.get(pk=input.id_animal_id.id_animal)
            if middleman_order_instance and input:
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
            id_order = input.id_order
            middleman_order_instance = MiddlemanOrder.objects.get(pk=id_order)
            if middleman_order_instance and input:
                for key, value in input.items():
                    setattr(middleman_order_instance, key, value)
                middleman_order_instance.save()
                ok = True
                return UpdateMiddlemanOrder(
                    ok=ok, middleman_order=middleman_order_instance, error=None
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
            return DeleteMiddlemanOrder(ok=ok, error="")
        except Exception as ex:
            return DeleteMiddlemanOrder(ok=ok, error=str(ex))


class Query(graphene.ObjectType):
    animal = Node.Field(LivestockNode)
    all_animals = DjangoFilterConnectionField(LivestockNode)
    middleman_order = Node.Field(MiddlemanOrderNode)
    all_middleman_orders = DjangoFilterConnectionField(MiddlemanOrderNode)
    customer_order = Node.Field(CustomerOrderNode)
    all_customer_orders = DjangoFilterConnectionField(CustomerOrderNode)
    users = Node.Field(UserNode)
    all_users = DjangoFilterConnectionField(UserNode)
    farm_order = Node.Field(FarmOrderNode)
    all_farm_orders = DjangoFilterConnectionField(FarmOrderNode)
    farm = Node.Field(FarmNode)
    all_farms = DjangoFilterConnectionField(FarmNode)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_farm_order = CreateFarmOrder.Field()
    update_farm_order = UpdateFarmOrder.Field()
    delete_farm_order = DeleteFarmOrder.Field()
    create_customer_order = CreateCustomerOrder.Field()
    update_customer_order = UpdateCustomerOrder.Field()
    delete_customer_order = DeleteCustomerOrder.Field()
    create_middleman_order = CreateMiddlemanOrder.Field()
    update_middleman_order = UpdateMiddlemanOrder.Field()
    delete_middleman_order = DeleteMiddlemanOrder.Field()
