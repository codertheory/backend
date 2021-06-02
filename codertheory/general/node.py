from graphene import Node


class BaseNode(Node):
    class Meta:
        name = "Node"

    # @classmethod
    # def to_global_id(cls, type, id):
    #     return id
    #
    # @classmethod
    # def from_global_id(cls, global_id):
    #     return None, global_id
