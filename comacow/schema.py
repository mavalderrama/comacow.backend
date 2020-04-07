from graphene import ObjectType, Schema
import comacow.polls.schema


class Query(comacow.polls.schema.Query, ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = Schema(query=Query)
