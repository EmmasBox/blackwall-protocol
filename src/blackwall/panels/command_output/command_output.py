
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.signal import Signal
from textual.widgets import Log


class PanelCommandOutput(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Log(id="tab_command_log")

    def on_mount(self) -> None:
        on_change: Signal[str] = self.app.command_output_change # type: ignore
        on_change.subscribe(node=self,callback=self.write_to_log)
        self.write_to_log(self.app.command_output) # type: ignore

    def write_to_log(self, output: str):
        log = self.get_child_by_id("tab_command_log",Log)
        log.clear()
        log.write(output)