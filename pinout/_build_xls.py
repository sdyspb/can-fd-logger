#!/usr/bin/env python3
"""Build FC7300F8MDT pinout .xls (one worksheet per functional block)."""
import re
from collections import Counter
import openpyxl

SRC = r'D:\work\!myprojects\canfd-logger-fc7300\pinout\FC7300F8MDT Pinout_V1.3.xlsx'
DST = r'D:\work\!myprojects\canfd-logger-fc7300\pinout\fc7300-320-pin.xlsx'

wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb['Pinout_FC7300F8MDT']

pins = []
for row in ws.iter_rows(min_row=2, values_only=True):
    lqfp = str(row[0]).strip() if row[0] is not None else ''
    bga = str(row[1]).strip() if row[1] is not None else ''
    name = str(row[2]).strip() if row[2] is not None else ''
    domain = str(row[3]).strip() if row[3] is not None else ''
    ptype = str(row[4]).strip() if row[4] is not None else ''
    if not bga and not lqfp:
        continue
    pins.append({'lqfp': lqfp, 'bga': bga, 'name': name,
                 'domain': domain, 'type': ptype,
                 'default': (str(row[5]).strip() if row[5] is not None else ''),
                 'alts': [str(c).strip() if c is not None else '' for c in row[6:14]]})

# BGA ball -> pin name
bm = wb['BGA_mapping']
ball2name = {}
for row in bm.iter_rows(min_row=2, max_row=21, values_only=True):
    rowlabel = str(row[0]).strip() if row[0] else ''
    if not re.fullmatch(r'[A-Z]', rowlabel):
        continue
    for col, cell in enumerate(row[1:21], start=1):
        val = str(cell).strip() if cell is not None else ''
        if val:
            ball2name[f'{rowlabel}{col}'] = val

def block_of(p):
    n = p['name']
    if n.startswith('VSS'):
        return 'Ground'
    if n.startswith('VDDA') or n.startswith('VREFH') or n.startswith('VREFL') \
            or n.startswith('V11_') or n.startswith('V15_') or n.startswith('V25') \
            or n in ('VDD_HV_A', 'VDD_HV_B', 'V15_CFG', 'V15_BASE_DRIVER'):
        return 'Power'
    if n in ('RESET_B', 'OSC32K_XTAL'):
        return 'Control'
    if re.fullmatch(r'PT[A-E]\d+', n):
        return 'GPIO'
    return 'Other'

ground = [p for p in pins if block_of(p) == 'Ground']
power = [p for p in pins if block_of(p) == 'Power']
gpio = [p for p in pins if block_of(p) == 'GPIO']
control = [p for p in pins if block_of(p) == 'Control']
other = [p for p in pins if block_of(p) == 'Other']
print(f'total {len(pins)} | ground {len(ground)} | power {len(power)} | gpio {len(gpio)} | control {len(control)} | other {len(other)}')
for p in power:
    print('  PWR', p['name'], 'LQFP', p['lqfp'], 'BGA', p['bga'], p['domain'])
for p in control:
    print('  CTL', p['name'], 'LQFP', p['lqfp'], 'BGA', p['bga'], p['type'])
for p in other:
    print('  OTH', p['name'], 'LQFP', p['lqfp'], 'BGA', p['bga'], p['domain'], p['type'])

c = Counter(p['name'] for p in pins)
print('duplicates:', {k: v for k, v in c.items() if v > 1})

# GPIO naming: duplicates -> ORIGINAL_n
seen = Counter(p['name'] for p in gpio)
for idx, p in enumerate(gpio):
    if seen[p['name']] > 1:
        n = sum(1 for q in gpio[:idx] if q['name'] == p['name'])
        p['out'] = f'{p["name"]}{n}'
    else:
        p['out'] = p['name']

def assign_side(rows):
    half = len(rows) // 2
    for i, r in enumerate(rows):
        r['side'] = 'LEFT' if i < half else 'RIGHT'

for blk in (ground, power, gpio, control):
    assign_side(blk)
    half = len(blk) // 2
    print(blk[0]['name'] if blk else '-', len(blk), 'LEFT:',
          [r['name'] for r in blk[:half]], 'RIGHT:', [r['name'] for r in blk[half:]])

# ---- duplicates in Ground/Power -> ORIGINAL_n ------------------------------
for blk in (ground, power):
    cnt = Counter(p['name'] for p in blk)
    for idx, p in enumerate(blk):
        if cnt[p['name']] > 1:
            n = sum(1 for q in blk[:idx] if q['name'] == p['name'])
            p['out'] = f'{p["name"]}_{n + 1}'
        else:
            p['out'] = p['name']
    for p in blk:
        if 'out' not in p:
            p['out'] = p['name']

def type_of(p):
    n = p['name']
    if n.startswith('VSS'):
        return 'GND'
    if not re.fullmatch(r'PT[A-T]\d+', n):
        return 'PWR'
    return 'BIDIR'

# ---- GPIO: name = pin name + all mux functions separated by '/' ------------
def sort_key(p):
    bank = p['name'][2]
    return (bank, int(p['name'][3:]), p['lqfp'] or '999')

for p in gpio:
    fns = [p['default']]
    for alt in p['alts']:
        if alt and alt not in fns:
            fns.append(alt)
    p['out'] = '/'.join(fns)

gpio = sorted(gpio, key=sort_key)

def side_of(p):
    if p in ground or p in power:
        return p['side']
    return 'Right'

# ---- write .xlsx (format per fx3.xlsx reference) ---------------------------
wb2 = openpyxl.Workbook()
wb2.remove(wb2.active)
DSTX = DST.replace('.xls', '.xlsx')
for sheet_name, items in [('GPIO', gpio), ('PWR', power), ('GND', ground)]:
    sh = wb2.create_sheet(sheet_name)
    for r, p in enumerate(items, start=1):
        sh.cell(row=r, column=1, value=p['out'])
        sh.cell(row=r, column=2, value=p['bga'])
        sh.cell(row=r, column=3, value=type_of(p))
        sh.cell(row=r, column=4, value=side_of(p))
        if p['lqfp']:
            sh.cell(row=r, column=5, value=p['lqfp'])
wb2.save(DSTX)
print('WROTE:', DSTX)

# verification
b2 = openpyxl.load_workbook(DSTX)
for s in b2.worksheets:
    print(s.title, s.max_row, 'rows,', s.max_column, 'cols')

