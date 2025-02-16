from textual.app import App
from textual.widgets import Header, Footer, Tabs, ListView, Input, Label, Tab

system_name = "TEST"

class Blackwall(App):
    #This portion handles the text in the header bar
    def on_mount(self) -> None:
        self.title = "Blackwall Protocol"
        self.sub_title = "Mainframe Security Administration"

    def compose(self):
        yield Label(f"You are working on mainframe system {system_name}")
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
