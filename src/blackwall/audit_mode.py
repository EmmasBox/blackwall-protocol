
from textual.app import ComposeResult
from textual.widgets import Label
from textual.containers import Container
import io
from datetime import datetime

try:
    from textual_image.widget import SixelImage
    image_enabled = True
except ImportError:
    print("##BLKWL_ERROR_3 Warning: could not find textual-image")    
    image_enabled = False

try:
    import qrcode
    qrcode_enabled = True
except ImportError:
    print("##BLKWL_ERROR_4 Warning: could not find qrcode")    
    qrcode_enabled = False

class AuditQRCode(Container):
    def compose(self) -> ComposeResult:
        now = datetime.now() # current date and time
        date_time = now.strftime("date: %m/%d/%Y time: %H:%M:%S")
        local_now = now.astimezone()
        local_tz = local_now.tzinfo
        local_tzname = local_tz.tzname(local_now)
        img = qrcode.make(f"{date_time} {local_tzname}")
        pil_image = img.get_image()
        yield Label("Audit mode")
        yield SixelImage(pil_image, classes="qrcode-image") # type: ignorez