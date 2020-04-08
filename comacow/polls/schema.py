import graphene

from graphene_django.types import DjangoObjectType, ObjectType

from .models import User, Farm, Livestock, FarmOrder, MiddlemanOrder, CustomerOrder


class UserType(DjangoObjectType):
    class Meta:
        model = User


class FarmType(DjangoObjectType):
    class Meta:
        model = Farm


class LivestockType(DjangoObjectType):
    class Meta:
        model = Livestock


class FarmOrderType(DjangoObjectType):
    class Meta:
        model = FarmOrder


class MiddlemanOrderType(DjangoObjectType):
    class Meta:
        model = MiddlemanOrder


class CustomerOrderType(DjangoObjectType):
    class Meta:
        model = CustomerOrder


class Query(ObjectType):
    user = graphene.Field(UserType, username=graphene.String())
    all_users = graphene.List(UserType)
    all_farms = graphene.List(FarmType)
    all_livestocks = graphene.List(LivestockType)
    all_farmorders = graphene.List(FarmOrderType)
    all_middlemanorders = graphene.List(MiddlemanOrderType)
    all_customerorders = graphene.List(CustomerOrderType)

    def resolve_user(self, info, **kwargs):
        print(kwargs)
        username = kwargs.get("username")
        return User.objects.get(username=username)

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_all_farms(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        # return Farm.objects.select_related('category').all()
        return Farm.objects.all()

    def resolve_all_livestocks(self, info, **kwargs):
        return Livestock.objects.all()

    def resolve_all_farmorders(self, info, **kwargs):
        return FarmOrder.objects.all()

    def resolve_all_middlemanorders(self, info, **kwargs):
        return MiddlemanOrder.objects.all()

    def resolve_all_customerorders(self, info, **kwargs):
        return CustomerOrder.objects.all()


class UserInput(graphene.InputObjectType):
    nit = graphene.String()
    email = graphene.String()
    username = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    user_type = graphene.String()
    phone = graphene.String()
    is_active = graphene.Boolean()


class CreateUser(graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        actor_instance = User(name=input.name)
        actor_instance.save()
        return CreateUser(ok=ok, actor=actor_instance)