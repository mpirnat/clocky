import board
import time

from adafruit_bitmap_font import bitmap_font
from adafruit_datetime import datetime, timedelta
from adafruit_display_text.label import Label
from adafruit_pyportal import PyPortal

UTC_OFFSET = -4

# the current working directory (where this file is)
cwd = ("/"+__file__).rsplit('/', 1)[0]
font = bitmap_font.load_font(cwd+"/fonts/Arial-ItalicMT-17.bdf")
font.load_glyphs("123456789-:")

pyportal = PyPortal(
    status_neopixel=board.NEOPIXEL,
    default_bg=cwd+"/clocky.bmp",
)

# local time
textarea = Label(font, text='YYYY-MM-DD HH:mm:SS')
textarea.x = 25
textarea.y = 58
textarea.color = 0xFFFFFF
pyportal.splash.append(textarea)

# utc time
textarea2 = Label(font, text='YYYY-MM-DD HH:mm:SS')
textarea2.x = 25
textarea2.y = 120
textarea2.color = 0xFFFFFF
pyportal.splash.append(textarea2)


refresh_time = None
while True:
    if (not refresh_time) or (time.monotonic() - refresh_time) > 3600:
        try:
            print("Getting time from internet!")
            pyportal.get_local_time()
            refresh_time = time.monotonic()
        except Exception as e:
            print("Some error occurred, retrying! -", e)
            time.sleep(5)
            continue

    now = datetime.now()
    utcnow = now - timedelta(hours=UTC_OFFSET)
    textarea.text = now.isoformat()
    textarea2.text = utcnow.isoformat()

    time.sleep(1)
