from textual.app import ComposeResult
from textual.widgets import Input, MaskedInput, Label, Button, RadioButton
from textual.containers import HorizontalGroup, VerticalGroup

class PanelUserName(HorizontalGroup):
    """Username and name components"""
    def compose(self) -> ComposeResult:
        yield Label("Username: ")
        yield Input(max_length=8,id="username",classes="username")
        yield Label("name: ")
        yield Input(max_length=20,id="name",classes="name")

class PanelUserOwnership(HorizontalGroup):
    """Component that contains ownership field and default group"""
    def compose(self) -> ComposeResult:
        yield Label("Owner: ")
        yield Input(max_length=8,id="owner",classes="owner")
        yield Label("Default group: ")
        yield Input(max_length=8,id="dfltgrp",classes="owner")

class PanelUserPassword(VerticalGroup):
    #Import css
    """Change/add password component"""
    def compose(self) -> ComposeResult:
        yield Label("Password:")
        yield Input(max_length=8,id="password",classes="password",password=True)
        yield Label("Repeat password:")
        yield Input(max_length=8,id="password_repeat",classes="password",password=True)

class PanelUserPassphrase(VerticalGroup):
    """Change/add passphrase component"""
    def compose(self) -> ComposeResult:
        yield Label("Passphrase:")
        yield Input(max_length=100,id="passphrase",classes="passphrase",password=True)
        yield Label("Repeat passphrase:")
        yield Input(max_length=100,id="passphrase_repeat",classes="passphrase",password=True)
    
class PanelUserAttributes(VerticalGroup):
    """User attributes component"""
    def compose(self) -> ComposeResult:
        yield Label("User attributes:")
        yield RadioButton("Special",id="user_attribute_special",tooltip="This is RACF's way of making a user admin. Special users can make other users special, making this a potentially dangerous option")
        yield RadioButton("Operations",id="user_attribute_operations",tooltip="This is a very dangerous attribute that allows you to bypass most security checks on the system, this should only be used during maintenance tasks and removed immediately afterwards")
        yield RadioButton("Auditor",id="user_attribute_auditor")
        yield RadioButton("Read only auditor (ROAUDIT)",id="user_attribute_roaudit")

class PanelUserSegments(VerticalGroup):
    """Component where the user can add segments such as the OMVS segment"""
    def compose(self) -> ComposeResult:
        yield Label("User segments:")
        yield RadioButton("TSO",id="user_segment_tso")
        yield RadioButton("OMVS",id="user_segment_omvs")
        yield RadioButton("CSDATA",id="user_segment_csdata")
        yield RadioButton("KERB",id="user_segment_kerb")
        yield RadioButton("LANGUAGE",id="user_segment_language")
        yield RadioButton("OPERPARM",id="user_segment_operparm")
        yield RadioButton("OVM",id="user_segment_ovm")
        yield RadioButton("NDS",id="user_segment_nds")
        yield RadioButton("DCE",id="user_segment_dce")
        yield RadioButton("DFP",id="user_segment_dfp")
        yield RadioButton("CICS",id="user_segment_cics")

