import channels_graphql_ws

from config.api import schema


class GraphQLConsumer(channels_graphql_ws.GraphqlWsConsumer):
    schema = schema
