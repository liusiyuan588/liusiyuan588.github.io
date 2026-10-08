"""Build original, schematic SVG art for the website (not experimental results)."""
import math
import random
from pathlib import Path

OUT = Path(__file__).parent / 'assets' / 'img'
OUT.mkdir(parents=True, exist_ok=True)


def mix(a, b, t):
    return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))


def hexrgb(rgb):
    return '#' + ''.join(f'{int(max(0,min(255,c))):02x}' for c in rgb)


def stops(t, positions):
    t=max(0,min(1,t))
    for i in range(len(positions)-1):
        p, c=positions[i]
        q, d=positions[i+1]
        if t <= q:
            return hexrgb(mix(c,d,(t-p)/(q-p)))
    return hexrgb(positions[-1][1])

PALETTE=[(0.,(28,52,65)),(.24,(64,100,123)),(.5,(139,164,154)),(.75,(227,192,123)),(1.,(242,123,92))]
COOL=[(0.,(15,23,37)),(.24,(49,73,99)),(.47,(75,112,123)),(.72,(145,170,147)),(1.,(198,239,108))]
WAVE=[(0.,(22,32,53)),(.3,(52,70,119)),(.53,(79,121,157)),(.8,(121,173,179)),(1.,(195,241,111))]

def header(w=1200,h=760, name='STUDY / 001'):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Illustrative scientific visualization">
<defs>
 <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#e5f7d8" opacity=".13"/></pattern>
 <linearGradient id="shade" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#12232d"/><stop offset="1" stop-color="#071016"/></linearGradient>
 <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#091116" stop-opacity="0"/><stop offset="1" stop-color="#091116" stop-opacity=".64"/></linearGradient>
</defs>
<rect width="{w}" height="{h}" fill="url(#shade)"/><rect width="{w}" height="{h}" fill="url(#dots)"/>
<path d="M 45 48 H {w-44} M 45 {h-46} H {w-44}" stroke="#d3e5d8" stroke-opacity=".23" stroke-width="1"/>
<g font-family="monospace" font-size="13" fill="#d4e9da" opacity=".8"><text x="47" y="32">{name}</text><text x="{w-266}" y="32">SCHEMATIC / NOT DATA</text><text x="47" y="{h-21}">NUMERICAL FIELDS</text><text x="{w-270}" y="{h-21}">COMPUTATIONAL MECHANICS ↗</text></g>'''

def close_svg(): return '</svg>'


def draw_stress():
    parts=[header(name='THERMOMECHANICS / 001')]
    x0,y0=98,151; nx,ny=56,27; cw,ch=1002/nx,425/ny
    for iy in range(ny):
        for ix in range(nx):
            x=(ix+.5)/nx; y=(iy+.5)/ny
            # thermomechanical discontinuity at layer interfaces + stress concentration near corner
            center=math.exp(-((x-.68)/.26)**2 - ((y-.59)/.35)**2)
            bend=math.exp(-((x-.13)/.13)**2 - ((y-.24)/.2)**2)
            layer= .21 if y<.27 else (-.12 if y<.62 else .17)
            v=.15+.57*center+.34*bend+layer+.09*math.sin(10*x-4*y)
            color=stops(v,PALETTE)
            xx=x0+ix*cw; yy=y0+iy*ch
            parts.append(f'<rect x="{xx:.1f}" y="{yy:.1f}" width="{cw+.3:.2f}" height="{ch+.3:.2f}" fill="{color}"/>')
    for i in range(0,nx+1,2):
        x=x0+i*cw
        parts.append(f'<path d="M{x:.1f} {y0}V{y0+ny*ch}" stroke="#0c1820" stroke-width=".65" opacity=".35"/>')
    for j in range(0,ny+1,2):
        y=y0+j*ch
        parts.append(f'<path d="M{x0} {y:.1f}H{x0+nx*cw}" stroke="#0c1820" stroke-width=".65" opacity=".35"/>')
    for yy in [y0+.27*ny*ch,y0+.62*ny*ch]:
        parts.append(f'<path d="M{x0} {yy:.1f}H{x0+nx*cw}" stroke="#efffe5" stroke-width="2" stroke-dasharray="9 5" opacity=".9"/>')
    parts += [f'<path d="M{x0} {y0} H{x0+nx*cw}V{y0+ny*ch}H{x0}Z" fill="none" stroke="#dce6dd" stroke-width="1.5" opacity=".9"/>',
             '<circle cx="784" cy="396" r="96" fill="none" stroke="#d4f89c" opacity=".8" stroke-width="1.6" stroke-dasharray="7 8"/>',
             '<path d="M835 325 L910 225 L1010 225" fill="none" stroke="#d4f89c" stroke-width="1.6"/>',
             '<g font-family="monospace" fill="#def0c6"><text x="920" y="213" font-size="18">σₓₓ</text><text x="920" y="240" font-size="12">LOCAL RESPONSE</text></g>',
             '<g fill="#d6e4dc" font-family="monospace" font-size="15"><text x="98" y="637">ELECTRODE</text><text x="465" y="637">ELECTROLYTE</text><text x="877" y="637">SUPPORT</text></g>',
             '<g stroke="#abbfaf" stroke-width="1.2" opacity=".7"><path d="M98 599 V620 M465 599 V620 M877 599 V620"/></g>']
    parts.append(close_svg()); (OUT/'solid-oxide-stress.svg').write_text(''.join(parts),encoding='utf-8')


def draw_phase():
    parts=[header(name='FRACTURE MECHANICS / 002')]
    x0,y0=86,123; w,h=1028,494; nx,ny=74,38
    for iy in range(ny):
        for ix in range(nx):
            x=(ix+.5)/nx; y=(iy+.5)/ny
            # mild heterogeneity and localization around a growing crack
            pathx=.28+.23*(y)+.045*math.sin(11*y)+.045*math.sin(19*y)
            damage=math.exp(-((x-pathx)/.017)**2)*(.98 if y<.83 else math.exp(-(y-.83)*45))
            wake=math.exp(-((x-pathx)/.066)**2)*.19
            background=.18+.09*math.sin(x*11)*math.sin(y*6)
            val=background+damage*.77+wake
            col=stops(val,COOL)
            parts.append(f'<rect x="{x0+ix*w/nx:.2f}" y="{y0+iy*h/ny:.2f}" width="{w/nx+.2:.2f}" height="{h/ny+.2:.2f}" fill="{col}"/>')
    for ix in range(0,nx+1,2):
        x=x0+ix*w/nx
        parts.append(f'<path d="M{x:.1f} {y0}V{y0+h}" stroke="#d8e3d2" stroke-opacity=".19" stroke-width=".7"/>')
    for iy in range(0,ny+1,2):
        y=y0+iy*h/ny
        parts.append(f'<path d="M{x0} {y:.1f}H{x0+w}" stroke="#d8e3d2" stroke-opacity=".19" stroke-width=".7"/>')
    crack=[]
    for i in range(64):
        y=i/75
        x=.28+.23*y+.045*math.sin(11*y)+.045*math.sin(19*y)
        crack.append(f'{x0+x*w:.1f},{y0+y*h:.1f}')
    parts.append('<polyline points="'+' '.join(crack)+'" fill="none" stroke="#d9f7a3" stroke-width="4" stroke-linecap="round"/>')
    parts += [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#eafbe4" stroke-width="1.4" opacity=".7"/>',
              '<path d="M570 418 L708 301 H947" stroke="#d7f4b2" stroke-width="1.5" stroke-dasharray="6 7" fill="none"/>',
              '<g font-family="monospace" fill="#deefcf"><text x="722" y="287" font-size="18">PHASE FIELD / d</text><text x="722" y="312" font-size="12">DIFFUSE CRACK BAND</text></g>',
              '<g font-family="monospace" fill="#bdcbbf" font-size="13"><text x="100" y="650">INTACT   →   DAMAGED</text><text x="835" y="650">INCREMENTAL LOADING</text></g>']
    parts.append(close_svg()); (OUT/'phase-field-fracture.svg').write_text(''.join(parts),encoding='utf-8')


def draw_fft():
    parts=[header(name='SPECTRAL COMPUTING / 003')]
    x0,y0=80,123; w,h=1040,490; nx,ny=82,43
    for iy in range(ny):
        for ix in range(nx):
            x=ix/nx; y=iy/ny
            signal=.5+.22*math.sin(2*math.pi*(3.3*x+1.1*y)) + .14*math.cos(2*math.pi*(1.3*x-4.2*y))+.11*math.sin(2*math.pi*(5*x+5*y))
            envelope=.22*math.exp(-((x-.64)/.2)**2-((y-.4)/.38)**2)
            color=stops(signal+envelope,WAVE)
            parts.append(f'<rect x="{x0+ix*w/nx:.2f}" y="{y0+iy*h/ny:.2f}" width="{w/nx+.5:.2f}" height="{h/ny+.5:.2f}" fill="{color}"/>')
    for ix in range(0,nx+1,4):
        x=x0+ix*w/nx
        parts.append(f'<path d="M{x:.1f} {y0}V{y0+h}" stroke="#e0fbe1" stroke-opacity=".25" stroke-width="1"/>')
    for iy in range(0,ny+1,4):
        y=y0+iy*h/ny
        parts.append(f'<path d="M{x0} {y:.1f}H{x0+w}" stroke="#e0fbe1" stroke-opacity=".25" stroke-width="1"/>')
    parts += [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#e3f9da" opacity=".65"/>',
              '<circle cx="866" cy="347" r="134" stroke="#ddfcae" stroke-width="1.5" stroke-dasharray="6 6" fill="none" opacity=".75"/>',
              '<circle cx="866" cy="347" r="73" stroke="#ddfcae" stroke-width="1.2" fill="none" opacity=".65"/>',
              '<path d="M866 212 V482 M730 347 H1002" stroke="#d9fcbb" opacity=".8" stroke-width="1"/>',
              '<g font-family="monospace" font-size="13" fill="#e0f1d5"><text x="100" y="654">FOURIER OPERATORS</text><text x="910" y="654">k-SPACE / FIELD</text></g>']
    parts.append(close_svg()); (OUT/'fft-computing.svg').write_text(''.join(parts),encoding='utf-8')


def draw_hero():
    w,h=870,1040
    parts=[f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Illustrative numerical mesh and localized strain field">
<defs>
 <radialGradient id="glow"><stop stop-color="#86ac81" stop-opacity=".38"/><stop offset=".5" stop-color="#51738d" stop-opacity=".12"/><stop offset="1" stop-color="#1a292f" stop-opacity="0"/></radialGradient>
 <pattern id="hero-grid" patternUnits="userSpaceOnUse" width="25" height="25"><path d="M25 0H0V25" fill="none" stroke="#a1babc" stroke-opacity=".12" stroke-width="1"/></pattern>
 <clipPath id="mask"><path d="M105 200 Q450 118 756 216 L755 785 Q436 880 105 778 Z"/></clipPath>
</defs>
<rect width="870" height="1040" fill="#0d161b"/>
<rect x="0" y="0" width="870" height="1040" fill="url(#hero-grid)"/>
<ellipse cx="504" cy="504" rx="440" ry="515" fill="url(#glow)"/>
<g font-family="monospace" fill="#b4c0b5" font-size="15"><text x="40" y="52">FIELD NOTES / 001</text><text x="654" y="52">FEM · 2D</text><text x="40" y="993">ILLUSTRATIVE / NOT RESULTS</text><text x="653" y="993">2026 / R&amp;D</text></g>
<path d="M40 77H830 M40 960H830" stroke="#9fad9c" stroke-opacity=".27" stroke-width="1"/>
<g clip-path="url(#mask)">''']
    x0,y0=105,165; nx=29; ny=34; dx=655/nx; dy=670/ny
    # gradient colored mesh: stress concentration near crack tip
    for iy in range(ny):
        for ix in range(nx):
            x=(ix+.5)/nx; y=(iy+.5)/ny
            tip=math.exp(-((x-.51)/.25)**2 - ((y-.55)/.22)**2)
            waves=.12*math.sin(12*x-9*y)+.08*math.cos(14*y+8*x)
            v=.18 + tip*.69 + waves + .18*(1-y)
            color=stops(v,PALETTE)
            px=x0+ix*dx; py=y0+iy*dy
            parts.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{dx+.3:.1f}" height="{dy+.3:.1f}" fill="{color}"/>')
    for iy in range(ny+1):
        coords=[]
        for ix in range(nx+1):
            x=ix/nx; y=iy/ny
            ux=18*math.exp(-((x-.53)/.33)**2)*math.sin(y*2*math.pi)
            uy=25*math.sin(math.pi*x)*math.sin(2*math.pi*y)
            coords.append(f'{x0+ix*dx+ux:.1f},{y0+iy*dy+uy:.1f}')
        parts.append('<polyline points="'+' '.join(coords)+'" fill="none" stroke="#d7e4ce" stroke-opacity=".23" stroke-width=".75"/>')
    for ix in range(nx+1):
        coords=[]
        for iy in range(ny+1):
            x=ix/nx; y=iy/ny
            ux=18*math.exp(-((x-.53)/.33)**2)*math.sin(y*2*math.pi)
            uy=25*math.sin(math.pi*x)*math.sin(2*math.pi*y)
            coords.append(f'{x0+ix*dx+ux:.1f},{y0+iy*dy+uy:.1f}')
        parts.append('<polyline points="'+' '.join(coords)+'" fill="none" stroke="#d7e4ce" stroke-opacity=".24" stroke-width=".75"/>')
    parts.append('</g>')
    parts += ['<path d="M105 200 Q450 118 756 216 L755 785 Q436 880 105 778 Z" fill="none" stroke="#d6e8ce" stroke-opacity=".72" stroke-width="2"/>',
              '<path d="M105 502 L283 501 Q326 489 365 515 Q394 549 432 562 Q463 549 483 512 L511 492 L539 464" fill="none" stroke="#d7ff87" stroke-width="4" stroke-linecap="round"/>',
              '<path d="M539 464 L648 356 H790" fill="none" stroke="#d7ff87" stroke-width="1.6" stroke-dasharray="5 6"/>',
              '<circle cx="539" cy="464" r="6" fill="#d7ff87"/><circle cx="539" cy="464" r="54" fill="none" stroke="#d7ff87" stroke-opacity=".7" stroke-width="1.4" stroke-dasharray="6 7"/>',
              '<g fill="#d7ff87" font-family="monospace"><text x="627" y="333" font-size="17">LOCALIZATION</text><text x="627" y="351" font-size="12">DAMAGE ONSET</text></g>',
              '<g font-family="monospace" fill="#c3cdc2" font-size="12" opacity=".95"><text x="95" y="891">σ / SIMULATED FIELD</text><text x="659" y="891">MESH 29 × 34</text></g>',
              '<g transform="translate(95 907)"><rect width="670" height="10" fill="#294458"/><rect width="180" height="10" x="170" fill="#76959b"/><rect width="180" height="10" x="340" fill="#d5b77e"/><rect width="150" height="10" x="520" fill="#ec8660"/></g>',
              '<g font-family="monospace" fill="#afc1b1" font-size="11"><text x="93" y="934">LOW</text><text x="721" y="934">HIGH</text></g>',close_svg()]
    (OUT/'hero-mesh.svg').write_text(''.join(parts),encoding='utf-8')


def favicon():
    svg='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="13" fill="#101715"/><path d="M13 22H51V28H33V49H26V28H13Z" fill="#cefa82"/><circle cx="49" cy="46" r="5" fill="#cefa82"/></svg>'''
    (OUT/'favicon.svg').write_text(svg,encoding='utf-8')

if __name__=='__main__':
    draw_stress(); draw_phase(); draw_fft(); draw_hero(); favicon()
    print('Generated original schematic SVG art in assets/img/')
