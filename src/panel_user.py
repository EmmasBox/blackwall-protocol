from textual.app import ComposeResult
from textual.widgets import Input, MaskedInput, Label, Button, Checkbox
from textual.containers import HorizontalGroup, VerticalScroll

class Panel_user_name(HorizontalGroup):
    """Username and name components"""
    CSS_PATH = "panel_user.tcss"
    def compose(self) -> ComposeResult:
        yield Label("Username: ")
        yield Input(max_length=8,id="username")
        yield Label("name: ")
        yield Input(max_length=20,id="name")

class Panel_user_ownership(HorizontalGroup):
    """Component that contains ownership field and default group"""
    CSS_PATH = "panel_user.tcss"
    def compose(self) -> ComposeResult:
        yield Label("Owner: ")
        yield Input(max_length=8,id="owner")
        yield Label("Default group: ")
        yield Input(max_length=8,id="dfltgrp")

class Panel_user_password():
    #Import css
    CSS_PATH = "panel_user.tcss"
    """Change/add password component"""
    def compose(self) -> ComposeResult:
        yield Label("Password:")
        yield MaskedInput(max_length=8,id="password")
        yield Label("Repeat password:")
        yield MaskedInput(max_length=8,id="password_repeat")

class Panel_user_passphrase():
    """Change/add passphrase component"""
    def compose(self) -> ComposeResult:
        yield Label("Passphrase:")
        yield MaskedInput(max_length=100,id="passphrase")
        yield Label("Repeat passphrase:")
        yield MaskedInput(max_length=100,id="passphrase_repeat")
    
class Panel_user_attributes():
    """User attributes component"""
    def compose(self) -> ComposeResult:
        yield Label("User attributes:")
        yield Checkbox("Special",id="user_attribute_special")
        yield Checkbox("Operations",id="user_attribute_operations")
        yield Checkbox("Auditor",id="user_attribute_auditor")
        yield Checkbox("Read only auditor (ROAUDIT)",id="user_attribute_roaudit")

class Panel_user_segments():
    """Component where the user can add segments such as the OMVS segment"""
    def compose(self) -> ComposeResult:
        yield Label("User segments:")
        yield Checkbox("OMVS",id="user_segment_omvs")

