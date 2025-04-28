
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.signal import Signal
from textual.widgets import Log


class PanelErrorHistory(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield Log(id="error_log")

    def on_mount(self) -> None:
        on_change: Signal[str] = self.app.error_output_change # type: ignore
        on_change.subscribe(node=self,callback=self.write_to_log)
        self.write_to_log(self.app.error_output) # type: ignore

    def write_to_log(self, output: str):
        log = self.get_child_by_id("#error_log",Log)
        log.clear()
        log.write(output)