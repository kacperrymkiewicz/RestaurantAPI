import graphene
import graphql_jwt
from .queries import Query as RootQuery
from api.graphql.mutations.mutations import Mutation as RootMutation


class Query(RootQuery, graphene.ObjectType):
    pass


class Mutation(RootMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
