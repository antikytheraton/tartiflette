from collections import OrderedDict
from typing import Dict, Optional

from tartiflette.types.field import GraphQLField
from tartiflette.types.type import GraphQLType


class GraphQLInterfaceType(GraphQLType):
    """
    Interface Type Definition

    It's an abstract type meaning that its purpose is to define a contract
    and enforce it on one or many fields of an Object type.
    The Interface type is used to describe what types are possible,
    what fields are in common across all types, as well as a
    function to determine which type is actually used
    when the field is resolved.
    """
    __slots__ = (
        'name',
        'description',
        '_fields',
    )

    def __init__(self, name: str, fields: Dict[str, GraphQLField],
                 description: Optional[str]=None):
        # In the function signature above, it should be `OrderedDict` but the
        # python 3.6 interpreter fails to interpret the signature correctly.
        super().__init__(name=name, description=description)
        # TODO: This will need a "resolve_type" function at execution time (?)
        self._fields: Dict[str, GraphQLField] = fields

    def __repr__(self) -> str:
        return "{}(name={!r}, fields={!r}, description={!r})".format(
            self.__class__.__name__,
            self.name, self._fields, self.description,
        )

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.fields == other.fields

    @property
    def fields(self) -> Dict[str, GraphQLField]:
        return self._fields

    @fields.setter
    def fields(self, value) -> None:
        self._fields = OrderedDict(value)
