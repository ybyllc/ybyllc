from pathlib import Path
from math import cos, sin, radians
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SIZE = 300
SCALE = 3
FPS = 4
DURATION = 60
BACKGROUND = '#f4f5f4'
TRACK = '#e0e2e0'
GREEN = '#7bc77e'
TEXT = '#202421'
label_font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 20 * SCALE)
clock_font = ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 40 * SCALE)
frames = []
for frame in range(DURATION * FPS):
    elapsed = frame / FPS
    if frame == DURATION * FPS - 1:
        elapsed = DURATION
    canvas = Image.new('RGB', (SIZE * SCALE, SIZE * SCALE), BACKGROUND)
    draw = ImageDraw.Draw(canvas)
    center = SIZE * SCALE / 2
    radius = 138 * SCALE
    stroke = 11 * SCALE
    bounds = (center - radius, center - radius, center + radius, center + radius)
    draw.ellipse(bounds, outline=TRACK, width=stroke)
    draw.ellipse((27 * SCALE, 27 * SCALE, 273 * SCALE, 273 * SCALE), fill='white')
    angle = elapsed / DURATION * 360
    if angle > 0:
        draw.arc(bounds, -90, -90 + angle, fill=GREEN, width=stroke)
        cap_radius = stroke / 2
        arc_radius = radius - stroke / 2
        for degrees in (-90, -90 + angle):
            px = center + arc_radius * cos(radians(degrees))
            py = center + arc_radius * sin(radians(degrees))
            draw.ellipse((px - cap_radius, py - cap_radius, px + cap_radius, py + cap_radius), fill=GREEN)
    seconds = int(elapsed)
    draw.text((center, 120 * SCALE), '你今天看了我几分钟', font=label_font, fill=TEXT, anchor='mm')
    draw.text((center, 174 * SCALE), f'{seconds // 60:02d}:{seconds % 60:02d}', font=clock_font, fill=TEXT, anchor='mm')
    frames.append(canvas.resize((SIZE, SIZE), Image.Resampling.LANCZOS))
destination = ROOT / 'assets' / 'profile-timer.gif'
destination.parent.mkdir(exist_ok=True)
palette = frames[DURATION * FPS // 4].quantize(colors=128)
frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
frames[0].save(destination, save_all=True, append_images=frames[1:], duration=1000 // FPS, loop=0, optimize=True, disposal=1)
with Image.open(destination) as result:
    assert result.n_frames == DURATION * FPS
    assert result.info['loop'] == 0
    total = 0
    for index in range(result.n_frames):
        result.seek(index)
        total += result.info['duration']
    assert total == DURATION * 1000
print(f'{destination}: 240 frames, 60 seconds, {destination.stat().st_size} bytes')
