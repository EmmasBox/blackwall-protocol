
from collections.abc import Generator
from dataclasses import Field, fields
from types import UnionType
from typing import get_args

from textual.widget import Widget
from textual.widgets import Collapsible, Input, Label, ListItem, ListView, RadioButton

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

def generate_trait_inputs(prefix: str, traits_class: type[TraitsBase],disabled: bool = False) -> Generator:
    for field in fields(traits_class):
        label = field.metadata.get("label")
        # only show an input field if it is labelled
        if label is not None:
            actual_type, optional = get_actual(field)

            input_args = field.metadata.get("input_args", {})

            input_id = f"{prefix}_{field.name}"

            if actual_type is str:
                yield Label(f"{label}{'*' if not optional else ''}:")
                yield Input(id=input_id, disabled=disabled, **input_args)
            elif actual_type is int:
                yield Label(f"{label}{'*' if not optional else ''}:")
                yield Input(id=input_id, type="integer", disabled=disabled, **input_args)
            elif actual_type == list[str]:
                with Collapsible(title=label,id=input_id):
                    yield ListView(disabled=disabled, **input_args)
            elif actual_type is bool:
                yield RadioButton(label=label, id=input_id, disabled=disabled, **input_args)

def generate_trait_section(title: str, prefix: str, traits_class: type[TraitsBase]) -> Generator:
    with Collapsible(title=title):
        yield from generate_trait_inputs(prefix=prefix,traits_class=traits_class)

def get_traits_from_input[T : TraitsBase](operator: str, widget: Widget, prefix: str, trait_cls: type[T]) -> T:
    value = trait_cls()
    for field in fields(trait_cls):
        actual_type, optional = get_actual(field)
        allowed_in = field.metadata.get("allowed_in")
        invalid_values = field.metadata.get("invalid_values")
        if allowed_in is not None and operator not in allowed_in:
            continue

        input_id = f"#{prefix}_{field.name}"
        label = field.metadata.get("label")
        if label is not None and actual_type != list[str]:
            field_value = widget.query_exactly_one(input_id).value # type: ignore
        else:
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

def toggle_inputs(widget: Widget, prefix: str, traits: TraitsBase, disabled: bool):
    for field in fields(type(traits)):
        actual_type, optional = get_actual(field)
        label = field.metadata.get("label")
        # Only toggle a field if it has a label
        if label is not None:
            input_id = f"#{prefix}_{field.name}"
            if (actual_type is str or actual_type is int or actual_type is bool):
                widget.query_exactly_one(selector=input_id).disabled = disabled

def set_traits_in_input(widget: Widget, prefix: str, traits: TraitsBase):
    for field in fields(type(traits)):
        actual_type, optional = get_actual(field)
        label = field.metadata.get("label")
        # only show an input field if it is labelled
        if label is not None:
            input_id = f"{prefix}_{field.name}"
            field_value = getattr(traits,field.name)
            if (actual_type is str or actual_type is int):
                if field_value is not None:
                    widget.query_exactly_one(f"#{input_id}").value = str(field_value) # type: ignore
            elif actual_type is bool:
                if field_value is not None:
                    widget.query_exactly_one(f"#{input_id}", RadioButton).value = field_value
            elif actual_type == list[str]:
                collapsible_widget = widget.get_child_by_id(input_id,expect_type=Collapsible)
                list_widget = collapsible_widget.get_child_by_type(Collapsible.Contents).get_child_by_type(ListView)
                if field_value is not None:
                    for item in field_value:
                        list_widget.append(ListItem(Label(item)))
