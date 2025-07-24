
from collections.abc import Generator
from dataclasses import Field, fields
from types import UnionType
from typing import get_args

from textual.widget import Widget
from textual.widgets import Collapsible, Input, Label, ListItem, ListView, RadioButton

from blackwall.api import user
from blackwall.api.traits_base import TraitsBase
from blackwall.panels.panel_mode import PanelMode
from blackwall.panels.users.user import PanelUser, UserInfo


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

def get_user_objects_for_panel(username: str) -> PanelUser:
    new_user_panel = PanelUser()

    user_dict = user.get_user(username)

    base_traits = user.BaseUserTraits.from_dict(prefix="base",source=user_dict["profile"]["base"])

    new_user_panel.user_info = UserInfo(
        base_traits=base_traits,
        username=username,
        mode=PanelMode.edit,
    )

    if 'profile' in user_dict and 'tso' in user_dict['profile']:
        new_user_panel.user_info.tso_traits = user.TSOUserTraits.from_dict(prefix="tso",source=user_dict["profile"]["tso"])

    if 'profile' in user_dict and 'omvs' in user_dict['profile']:
        new_user_panel.user_info.omvs_traits = user.OMVSUserTraits.from_dict(prefix="omvs",source=user_dict["profile"]["omvs"])

    if 'profile' in user_dict and 'nds' in user_dict['profile']:
        new_user_panel.user_info.nds_traits = user.NDSUserTraits.from_dict(prefix="nds",source=user_dict["profile"]["nds"])

    if 'profile' in user_dict and 'cics' in user_dict['profile']:
        new_user_panel.user_info.cics_traits = user.CICSUserTraits.from_dict(prefix="cics",source=user_dict["profile"]["cics"])

    if 'profile' in user_dict and 'netview' in user_dict['profile']:
        new_user_panel.user_info.netview_traits = user.NetviewUserTraits.from_dict(prefix="netview",source=user_dict["profile"]["netview"])

    if 'profile' in user_dict and 'mfa' in user_dict['profile']:
        new_user_panel.user_info.mfa_traits = user.MfaUserTraits.from_dict(prefix="mfa",source=user_dict["profile"]["mfa"])
    
    if 'profile' in user_dict and 'eim' in user_dict['profile']:
        new_user_panel.user_info.eim_traits = user.EIMUserTraits.from_dict(prefix="eim",source=user_dict["profile"]["eim"])

    if 'profile' in user_dict and 'workattr' in user_dict['profile']:
        new_user_panel.user_info.workattr_traits = user.WorkattrUserTraits.from_dict(prefix="workattr",source=user_dict["profile"]["workattr"])
    
    if 'profile' in user_dict and 'ovm' in user_dict['profile']:
        new_user_panel.user_info.ovm_traits = user.OvmUserTraits.from_dict(prefix="ovm",source=user_dict["profile"]["ovm"])

    if 'profile' in user_dict and 'dce' in user_dict['profile']:
        new_user_panel.user_info.dce_traits = user.DCEUserTraits.from_dict(prefix="dce",source=user_dict["profile"]["dce"])
    
    if 'profile' in user_dict and 'dfp' in user_dict['profile']:
        new_user_panel.user_info.dfp_traits = user.DFPUserTraits.from_dict(prefix="dfp",source=user_dict["profile"]["dfp"])

    if 'profile' in user_dict and 'operparm' in user_dict['profile']:
        new_user_panel.user_info.operparm_traits = user.OperparmUserTraits.from_dict(prefix="operparm",source=user_dict["profile"]["operparm"])

    if 'profile' in user_dict and 'proxy' in user_dict['profile']:
        new_user_panel.user_info.proxy_traits = user.ProxyUserTraits.from_dict(prefix="proxy",source=user_dict["profile"]["proxy"])
    
    if 'profile' in user_dict and 'lnotes' in user_dict['profile']:
        new_user_panel.user_info.lnotes_traits = user.LnotesUserTraits.from_dict(prefix="lnotes",source=user_dict["profile"]["lnotes"])

    if 'profile' in user_dict and 'language' in user_dict['profile']:
        new_user_panel.user_info.lang_traits = user.LanguageUserTraits.from_dict(prefix="language",source=user_dict["profile"]["language"])

    if 'profile' in user_dict and 'kerb' in user_dict['profile']:
        new_user_panel.user_info.kerb_traits = user.KerbUserTraits.from_dict(prefix="kerb",source=user_dict["profile"]["kerb"])

    return new_user_panel