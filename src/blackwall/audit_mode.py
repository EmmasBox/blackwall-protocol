
import importlib.util
from datetime import datetime

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label

#Checks if textual_image can be imported
image_enabled = importlib.util.find_spec('textual_image')

if image_enabled:
    from textual_image.widget import SixelImage
else:
    print("##BLKWL_ERROR_3 Warning: could not find textual-image")    

#Checks if qrcode can be imported
qrcode_enabled = importlib.util.find_spec('qrcode')

if qrcode_enabled:
    import qrcode  # type: ignore
else:
    print("##BLKWL_ERROR_4 Warning: could not find qrcode")   

class AuditQRCode(Container):
    def compose(self) -> ComposeResult:
        now = datetime.now() # current date and time
        date_time = now.strftime("date: %m/%d/%Y time: %H:%M:%S")
        local_now = now.astimezone()
        local_tz = local_now.tzinfo
        local_tzname = local_tz.tzname(local_now)
        
        yield Label("Audit mode")
        if qrcode_enabled and image_enabled:
            img = qrcode.make(f"{date_time} {local_tzname}")
            pil_image = img.get_image()
            yield SixelImage(pil_image, classes="qrcode-image") # type: ignorez