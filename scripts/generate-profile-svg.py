from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 300 300" role="img" aria-labelledby="title description">
  <title id="title">你今天看了我几分钟</title>
  <desc id="description">圆圈从十二点顺时针每秒增加，六十秒后保持满圈，时分秒继续累计。这是播放计时动画。</desc>
  <defs><clipPath id="clock"><rect x="52" y="145" width="196" height="43"/></clipPath></defs>
  <circle cx="150" cy="150" r="128" fill="#ffffff"/>
  <circle cx="150" cy="150" r="132.5" fill="none" stroke="#e0e2e0" stroke-width="11"/>
  <circle cx="150" cy="150" r="132.5" fill="none" stroke="#7bc77e" stroke-width="11" stroke-linecap="round" pathLength="60" stroke-dasharray="60 60" stroke-dashoffset="60" transform="rotate(-90 150 150)" visibility="hidden">
    <set attributeName="visibility" to="visible" begin="1s" fill="freeze"/>''']
values = ';'.join(str(60 - second) for second in range(61))
times = ';'.join(format(second / 60, '.10g') for second in range(61))
parts.append(f'    <animate attributeName="stroke-dashoffset" values="{values}" keyTimes="{times}" dur="60s" calcMode="discrete" repeatCount="1" fill="freeze"/>')
parts.append('''  </circle>
  <text x="150" y="127" text-anchor="middle" font-family="Microsoft YaHei, Noto Sans CJK SC, sans-serif" font-size="20" fill="#202421">你今天看了我几分钟</text>
  <g clip-path="url(#clock)" font-family="Arial, Helvetica, sans-serif" font-size="36" fill="#202421" text-anchor="middle">''')
for x in (117.5, 182.5):
    parts.append(f'    <text x="{x}" y="178">:</text>')
for x, count, seconds in [(74.5, 10, 36000), (96, 10, 3600), (139, 6, 600), (160.5, 10, 60), (204, 6, 10), (225.5, 10, 1)]:
    offsets = ';'.join(f'0 {-digit * 50}' for digit in range(count))
    key_times = ';'.join(format(digit / count, '.10g') for digit in range(count))
    parts.append(f'    <g transform="translate({x} 178)"><g>')
    for digit in range(count):
        parts.append(f'      <text x="0" y="{digit * 50}">{digit}</text>')
    parts.append(f'      <animateTransform attributeName="transform" type="translate" values="{offsets}" keyTimes="{key_times}" dur="{count * seconds}s" calcMode="discrete" repeatCount="indefinite"/>')
    parts.append('    </g></g>')
parts.append('  </g>\n</svg>\n')
svg = '\n'.join(parts)
ElementTree.fromstring(svg)
destination = ROOT / 'assets' / 'profile-timer.svg'
destination.write_text(svg, encoding='utf-8')
print(f'{destination}: transparent exterior, 240px, one step per second, ring freezes at 60s')
