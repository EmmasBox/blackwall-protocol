import importlib.util
import json
from datetime import datetime

from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.widgets import Digits, Label

from blackwall.settings import get_user_setting

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

class SystemInfo(HorizontalGroup):
    now = datetime.now() # current date and time
    local_now = now.astimezone()
    local_tz = local_now.tzinfo
    if local_tz is not None:
        local_tzname = local_tz.tzname(local_now)

    clock_enabled = get_user_setting(section="display",setting="system_clock")

    def compose(self) -> ComposeResult:
        if get_user_setting(section="display",setting="system_clock") is not False:
            yield Digits("", id="system_clock")
            yield Label(f"{str(self.local_tzname)} |",id="system_timezone")
        if zoau_enabled:
            system_label = get_user_setting(section="display",setting="system_label")
            if system_label is not False:
                if get_user_setting(section="display",setting="short_system_label"):
                    yield Label(f"System: {system_name}, LPAR: {lpar_name}",id="system_label",classes="system-label")
                else:
                    yield Label(f"You are working on the {system_name} mainframe system in LPAR {lpar_name}",id="system_label",classes="system-label")

    def on_mount(self) -> None:
        self.update_clock()
        if self.clock_enabled is not False:
            self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        if self.clock_enabled is not False:
            clock = datetime.now().time()
            self.get_child_by_id("system_clock",Digits).update(f"{clock:%T}")