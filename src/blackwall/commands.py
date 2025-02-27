from . import commands_definition as defintion
from textual.app import ComposeResult

from textual import on
from textual.widgets import Input, Label
from textual.containers import HorizontalGroup

try:
    from zoautil_py import mvscmd # type: ignore
    zoau_enabled = True
except:
    print("##BLKWL_ERROR_1 Warning: could not find ZOAU, disabling MVS commands")    
    zoau_enabled = False

class MVSCommandField(HorizontalGroup):
    def compose(self) -> ComposeResult:
        if zoau_enabled:
            yield Input(id="cli",max_length=250,classes="commands")
        else:
            yield Label("Install ZOAU to access MVS command field")

    @on(Input.Submitted)
    def execute_command(self) -> None:
        command = self.query_exactly_one(selector="#cli").value
        if command != "":
            output = mvscmd.execute(command)
            self.notify(f"command submitted: {output}")