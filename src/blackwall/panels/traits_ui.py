
from collections.abc import Generator
from dataclasses import fields, Field
from types import UnionType
from typing import get_args

from textual.lazy import Lazy
from textual.widget import Widget
from textual.widgets import Input, Label, RadioButton, Collapsible
from blackwall.api.traits_base import TraitsBase

def get_actual(field: Field) -> tuple[type,bool]:
    # UnionType is 'str | None'
    if isinstance(field.type, UnionType):
        # parse out actual type out of optional type
        # will be tuple (type(str), type(None))
        args = get_args(field.type)
        # the field is optional if type args contains 'type(None)'
        optional = type(None) in args
        # the actual type is the first non-'type(None)' in args
        actual_type = next((t for t in args if t is not type(None)), field.type)
    else:
        optional = False
        actual_type = field.type
    return actual_type, optional

def generate_trait_inputs(title: str, prefix: str, traits_class: type[TraitsBase]) -> Generator:
    with Lazy(widget=Collapsible(title=title)):
        for field in fields(traits_class):
            label = field.metadata.get("label")
            # only show an input field if it is labelled
            if label is not None:
                actual_type, optional = get_actual(field)

                input_args = field.metadata.get("input_args", {})

                input_id = f"{prefix}_{field.name}"

                if actual_type is str:
                    yield Label(f"{label}{'*' if not optional else ''}:")
                    yield Input(id=input_id, **input_args)
                elif actual_type is int:
                    yield Label(f"{label}{'*' if not optional else ''}:")
                    yield Input(id=input_id, type="integer", **input_args)
                elif actual_type is bool:
                    yield RadioButton(label=label, id=input_id, **input_args)

def get_traits_from_input(operator: str, widget: Widget, prefix: str, trait_cls: TraitsBase):
    value = trait_cls()
    for field in fields(trait_cls):
        actual_type, optional = get_actual(field)
        allowed_in = field.metadata.get("allowed_in")
        invalid_values = field.metadata.get("invalid_values")
        if allowed_in is not None and operator not in allowed_in:
            continue

        input_id = f"#{prefix}_{field.name}"
        try:
            field_value = widget.query_exactly_one(selector=input_id).value
        except:
            field_value = None

        if actual_type is str:
            if field_value == "":
                field_value = None
        elif actual_type is int:
            if field_value == "" or field_value == 0 or field_value is None:
                field_value = None
            else:
                field_value = int(field_value)

        if invalid_values is not None and field_value in invalid_values: 
            field_value = None

        setattr(value, field.name, field_value)
    return value