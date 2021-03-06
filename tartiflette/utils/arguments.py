import asyncio

from functools import partial
from typing import Any, Callable, Dict, List, Optional

from tartiflette.types.helpers import reduce_type
from tartiflette.types.input_object import GraphQLInputObjectType

UNDEFINED_VALUE = object()


def surround_with_argument_execution_directives(
    func: Callable, directives: List[Dict[str, Any]]
) -> Callable:
    for directive in reversed(directives):
        func = partial(
            directive["callables"].on_argument_execution,
            directive["args"],
            func,
        )
    return func


async def argument_coercer(argument_definition, args, ctx, info):
    value = UNDEFINED_VALUE
    try:
        value = args[argument_definition.name]
    except KeyError:
        pass

    if value is UNDEFINED_VALUE and argument_definition.default_value:
        value = argument_definition.default_value

    if value is UNDEFINED_VALUE:
        return value

    try:
        value = value.value
    except AttributeError:
        pass

    schema_type = argument_definition.schema.find_type(
        reduce_type(argument_definition.gql_type)
    )

    if not isinstance(schema_type, GraphQLInputObjectType):
        return value

    return await coerce_arguments(schema_type.arguments, value, ctx, info)


async def coerce_arguments(
    argument_definitions: Dict[str, "GraphQLArgument"],
    input_args: Dict[str, Any],
    ctx: Optional[Dict[str, Any]],
    info: "Info",
) -> Dict[str, Any]:
    results = await asyncio.gather(
        *[
            argument_definition.coercer(input_args, ctx, info)
            for argument_definition in argument_definitions.values()
        ]
    )

    return {
        argument_name: result
        for argument_name, result in zip(argument_definitions, results)
        if result is not UNDEFINED_VALUE
    }
