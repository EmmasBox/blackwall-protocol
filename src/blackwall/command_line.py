
from textual.app import ComposeResult

from datetime import datetime

from textual.suggester import SuggestFromList
from textual import on
from textual.events import ScreenResume
from textual.widgets import Input, Log, Label
from textual.containers import HorizontalGroup, VerticalGroup
from textual.screen import Screen

import subprocess

from blackwall.commands_definition import commands

from blackwall.messages import CommandHistory

command_history = ""

def generate_command_meta_header(command):
    now = datetime.now() # current date and time
    date_time = now.strftime("date: %m/%d/%Y time: %H:%M:%S")
    local_now = now.astimezone()
    local_tz = local_now.tzinfo
    local_tzname = local_tz.tzname(local_now)
    
    return f"""
    --------------------------------------------------------------------------------------------------
    Command '{command}' 
    executed on {date_time} {local_tzname}
    --------------------------------------------------------------------------------------------------
    \n
    """

class CommandHistoryWidget(VerticalGroup):
    def compose(self) -> ComposeResult:
        yield Label("Command history: ")
        yield Log()

class CommandHistoryScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
        yield CommandHistoryWidget()

    @on(ScreenResume)
    def on_resume(self):
        log = self.query_one(Log)
        log.clear()
        log.write(command_history)

class TSOCommandField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Input(id="cli",max_length=250,placeholder="Submit a TSO/RACF command...",classes="commands",suggester=SuggestFromList(commands,case_sensitive=False),tooltip="Use this command field to submit TSO and RACF commands. You can view the output in the command history panel")

    @on(Input.Submitted)
    def execute_command(self) -> None:
        global command_history
        command = self.query_exactly_one(selector="#cli").value
        if command != "":
            try:
                output = subprocess.run(f'tsocmd "{command}"' , shell=True, check=True, capture_output=True,encoding="utf-8")
                command_history = command_history + generate_command_meta_header(command) + output.stdout
                self.notify(f"command {command.upper()} successfully completed",severity="information")
                self.post_message(CommandHistory(command_history))
            except BaseException as e:
                self.notify(f"Command {command.upper()} failed: {e}",severity="error")