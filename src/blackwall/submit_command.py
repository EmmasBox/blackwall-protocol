
from datetime import datetime

import subprocess

def generate_command_meta_header(command: str) -> str:
    now = datetime.now() # current date and time
    date_time = now.strftime("date: %m/%d/%Y time: %H:%M:%S")
    local_now = now.astimezone()
    local_tz = local_now.tzinfo
    if local_tz is not None:
        local_tzname = local_tz.tzname(local_now)
        if local_tzname is not None:
            date_time = date_time + local_tzname
    
    return f"""
    --------------------------------------------------------------------------------------------------
    Command '{command}' 
    executed on {date_time}
    --------------------------------------------------------------------------------------------------
    \n
    """

def execute_command(command: str) -> str | None:
    output = subprocess.run(f'tsocmd "{command}"', text=False, shell=True, check=True, capture_output=True)
    return generate_command_meta_header(command) + output.stdout.decode("utf-8", errors="ignore")