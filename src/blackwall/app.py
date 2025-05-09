

from textual.app import App
from textual.containers import Container
from textual.signal import Signal
from textual.widgets import Footer, Header, Input

from blackwall.messages import SubmitCommand
from blackwall.notifications import send_notification
from blackwall.secret_scrubber import remove_secret
from blackwall.settings import get_site_setting, get_user_setting
from blackwall.submit_command import execute_command

from .command_line import CommandLine
from .screens.modal.refresh import RefreshScreen
from .screens.modal.rvary import RvaryScreen
from .system_info import SystemInfo
from .tabs import TabSystem
from .themes.theme_blackwall import blackwall_theme
from .themes.theme_cynosure import cynosure_theme


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
        self.register_theme(blackwall_theme)

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
                    scrubbed_command = remove_secret(string_input=message.command)
                    self.notify(f"command {scrubbed_command.upper()} successfully completed",severity="information")
            except BaseException as e:
                send_notification(self,message=f"Command {message.command.upper()} failed: {e}",severity="error")
                
    #UI elements
    def compose(self):
        #display system and LPAR name
        yield Header()
        yield SystemInfo()
        yield CommandLine()
        with Container():
            yield TabSystem()
        yield Footer()
