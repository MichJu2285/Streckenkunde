from PIL import Image, ImageDraw, ImageFont
import os

S = 180
img = Image.new("RGB", (S, S), (255, 255, 255))
d = ImageDraw.Draw(img)

# Roter Rand: abgerundetes Rechteck, mittlere Dicke (9 px bei 180 px)
d.rounded_rectangle([3, 3, S - 4, S - 4], radius=40, outline=(236, 0, 22), width=9)

# SK in Rot, mittig, fett
font = None
for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
    if os.path.exists(p):
        font = ImageFont.truetype(p, 74)
        break
if font is None:
    font = ImageFont.load_default()
try:
    d.text((S / 2, S / 2), "SK", font=font, fill=(236, 0, 22), anchor="mm")
except TypeError:
    bbox = d.textbbox((0, 0), "SK", font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text(((S - w) / 2 - bbox[0], (S - h) / 2 - bbox[1]), "SK", font=font, fill=(236, 0, 22))

img.save("icon.png")
print("icon.png geschrieben:", os.path.getsize("icon.png"), "Bytes")
