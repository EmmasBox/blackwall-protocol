from textual.app import App
from textual.widgets import Header, Footer, Tabs, ListView, Input, Label, Tab
from zoautil_py import zsystem
import json

zsystem_info = json.loads(zsystem.zinfo())

system_name = zsystem_info["sys_info"]["sys_name"]
lpar_name = zsystem_info["sys_info"]["lpar_name"]

class Blackwall(App):
    #This portion handles the text in the header bar
    def on_mount(self) -> None:
        self.title = "Blackwall Protocol"
        self.sub_title = "Mainframe Security Administration"

    def compose(self):
        yield Label(f"You are working on the {system_name} mainframe system in LPAR {lpar_name}")
        yield Input()
        yield Header()
        yield Tabs(
            Tab("Dataset profiles", id="one"),
            Tab("Resource profiles", id="two"),
            Tab("User profiles", id="three"),
            Tab("Statistics", id="four"),
        )
        yield ListView()
        yield Footer()

Blackwall().run()
