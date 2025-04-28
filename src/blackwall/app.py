
import importlib.util
import json

from textual.app import App
from textual.containers import Container
from textual.signal import Signal
from textual.widgets import Footer, Header, Input, Label

from blackwall.messages import SubmitCommand
from blackwall.notifications import send_notification
from blackwall.settings import get_site_setting, get_user_setting
from blackwall.submit_command import execute_command

from .command_line import CommandLine
from .screens.modal.refresh import RefreshScreen
from .screens.modal.rvary import RvaryScreen
from .tabs import TabSystem
from .theme_3270 import ibm_3270_theme
from .theme_cynosure import cynosure_theme

zoau_enabled = importlib.util.find_spec('zoautil_py')

if zoau_enabled:
    from zoautil_py import zsystem  # type: ignore
else:
    print("##BLKWL_ERROR_1 Warning: could not find ZOAU, certain features will be disabled such as diplaying system and LPAR names")    

command_history = ""

#system information
if zoau_enabled:
    zsystem_info = json.loads(zsystem.zinfo()) # type: ignore
    system_name = zsystem_info["sys_info"]["sys_name"]
    lpar_name = zsystem_info["sys_info"]["lpar_name"]

class Blackwall(App):
    #Import css
    CSS_PATH = "UI.css"

    BINDINGS = [
        ("h", "push_screen('refresh')", "Switch to refresh screen"),
        ("r", "push_screen('rvary')", "Switch to rvary password screen"),
        ("ctrl+home", "go_to_cli", "Focus command line"),
    ]
    
    #This portion handles the text in the header bar
    def on_mount(self) -> None:
        self.title = "Blackwall Protocol"
        site_company = get_site_setting(section="meta",setting="company")
        if site_company is not None and site_company != "":
            self.sub_title = f"Mainframe Security Administration at {site_company}"
        else:
            self.sub_title = "Mainframe Security Administration"
        self.register_theme(cynosure_theme)
        #self.register_theme(ibm_3270_theme)
        user_theme = get_user_setting(section="display",setting="theme")
        if user_theme is not None or user_theme == "":
            try:
                self.theme = user_theme
            except ImportError:
                self.notify("Couldn't find user theme",severity="warning")
        else:
            self.theme = "cynosure"
        self.install_screen(RefreshScreen(), name="refresh")
        self.install_screen(RvaryScreen(), name="rvary")

        self.command_output_change = Signal(self,name="command_output_change")
        self.command_output = ""

        self.error_output_change = Signal(self,name="error_output_change")
        self.error_output = ""

    async def action_go_to_cli(self) -> None:
        """Focuses the command line"""
        cli = self.get_child_by_type(CommandLine).get_child_by_type(Input)
        cli.focus()

    async def on_submit_command(self, message: SubmitCommand) -> None:
        """Executes command from message"""
        if message.command != "":
            try:
                output = execute_command(message.command)
                if output is not None:
                    self.command_output = self.command_output + output
                    self.command_output_change.publish(data=self.command_output)
                    self.notify(f"command {message.command.upper()} successfully completed",severity="information")
            except BaseException as e:
                send_notification(self,message=f"Command {message.command.upper()} failed: {e}",severity="error")
                
    #UI elements
    def compose(self):
        #display system and LPAR name
        yield Header()
        if zoau_enabled:
            system_label = get_user_setting(section="display",setting="system_label")
            if system_label is not False:
                if get_user_setting(section="display",setting="short_system_label"):
                    yield Label(f"System: {system_name}, LPAR: {lpar_name}",classes="system-label")
                else:
                    yield Label(f"You are working on the {system_name} mainframe system in LPAR {lpar_name}",classes="system-label")
        yield CommandLine()
        with Container():
            yield TabSystem()
        yield Footer()
