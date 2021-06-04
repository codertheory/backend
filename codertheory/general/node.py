from graphene import relay
from graphql import ResolveInfo


class BaseNode(relay.Node):

    @classmethod
    def get_node_from_global_id(cls, info: ResolveInfo, global_id, only_type=None):
        try:
            _type, _id = cls.from_global_id(global_id)
            if _type is None:
                _type = str(info.return_type)
            graphene_type = info.schema.get_type(_type).graphene_type
        except Exception as error:
            print(error, global_id, info)
            return None

        if only_type:
            assert graphene_type == only_type, "Must receive a {} id.".format(
                only_type._meta.name
            )

        # We make sure the ObjectType implements the "Node" interface
        if cls not in graphene_type._meta.interfaces:
            return None

        get_node = getattr(graphene_type, "get_node", None)
        if get_node:
            return get_node(info, _id)

    @classmethod
    def to_global_id(cls, type, id):
        return id

    @classmethod
    def from_global_id(cls, global_id):
        return None, global_id
