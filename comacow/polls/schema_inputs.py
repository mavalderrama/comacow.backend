import graphene


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


class FarmInput(graphene.InputObjectType):
    id_farm = graphene.ID()
    id_user_id = graphene.Field(UserInput)
    n_cow = graphene.Int()
    n_bull = graphene.Int()
    n_calf = graphene.Int()


class LivestockInput(graphene.InputObjectType):
    id_animal = graphene.ID()
    id_farm_id = graphene.Field(FarmInput)
    chapeta = graphene.String()
    animal_type = graphene.String()
    status = graphene.String()
    price = graphene.Float()
    raze = graphene.String()
    weight = graphene.Float()


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
