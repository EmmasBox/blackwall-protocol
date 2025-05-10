
from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.suggester import SuggestFromList
from textual.widgets import Input

from blackwall.commands_definition import commands
from blackwall.messages import SubmitCommand
from blackwall.secret_scrubber import remove_secret
from blackwall.settings import get_user_setting


class CommandLine(HorizontalGroup):
    BINDINGS = [
        ("up", "cycle_up", "Cycle previous executed commands"),
        ("down", "cycle_down", "Cycle previous executed commands"),
    ]

    command_history_list = []
    current_command_history_entry = -1

    def compose(self) -> ComposeResult:
        yield Input(id="cli",max_length=250,placeholder="Submit a TSO/RACF command...",classes="commands",suggester=SuggestFromList(commands,case_sensitive=False),tooltip="Use this command field to submit TSO and RACF commands. You can view the output in the command output tab.")

    @on(Input.Submitted)
    def submit_command(self) -> None:
        command_line = self.get_child_by_id("cli",Input)
        command = command_line.value
        self.post_message(SubmitCommand(command))
        clear_on_submission = get_user_setting(section="commands",setting="clear_on_submission")
        scrubbed_command = remove_secret(string_input=command)
        self.command_history_list.append(scrubbed_command)
        if clear_on_submission is not False:
            command_line.value = ""

    def action_cycle_up(self) -> None:
        if len(self.command_history_list) > 0:
            command_line = self.get_child_by_id("cli",Input)
            command_line.value = self.command_history_list[self.current_command_history_entry]
            if self.current_command_history_entry < len(self.command_history_list) -1:
                self.current_command_history_entry = self.current_command_history_entry + 1

    def action_cycle_down(self) -> None:
        if len(self.command_history_list) > 0:
            command_line = self.get_child_by_id("cli",Input)
            command_line.value = self.command_history_list[self.current_command_history_entry]
            if self.current_command_history_entry > -1:
                self.current_command_history_entry = self.current_command_history_entry - 1