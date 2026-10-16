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
    if name == 'RESET_b':
        # dedicated reset pin: not in BGA_mapping (no ball coordinate),
        # BGA ball B5 is taken from the main table
        pins.append({'lqfp': lqfp, 'bga': bga, 'name': 'RESET_B',
                     'domain': domain, 'type': ptype,
                     'default': 'RESET_B', 'alts': []})
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

# balls of a given net, in BGA_mapping grid order (row by row)
def balls_of(net):
    out = []
    for row in bm.iter_rows(min_row=2, max_row=21, values_only=True):
        rowlabel = str(row[0]).strip() if row[0] else ''
        if not re.fullmatch(r'[A-Z]', rowlabel):
            continue
        for col, cell in enumerate(row[1:21], start=1):
            val = str(cell).strip() if cell is not None else ''
            if val == net:
                out.append(f'{rowlabel}{col}')
    return out

VSS_BALLS = balls_of('VSS')
HV_A_BALLS = balls_of('VDD_HV_A')
HV_B_BALLS = balls_of('VDD_HV_B')
print('VSS balls:', len(VSS_BALLS), VSS_BALLS)
print('HV_A balls:', len(HV_A_BALLS), HV_A_BALLS)
print('HV_B balls:', len(HV_B_BALLS), HV_B_BALLS)

# ---- shared ball pools (in order of appearance in the main table) ----------
# NOTE: the V1.3 main table lists 10 VDD_HV_A pins, but BGA_mapping has only 6
# real VDD_HV_A balls. The datasheet is ambiguous here — the 4 extra LQFP
# positions (110/126/141/151) are kept with the 'VDD_HV_A' marker, their real
# coordinates are unknown from this file.
# NOTE (rule "Parsing repeated nets" p.3): the V1.3 main table lists 14 VSS
# rows, but BGA_mapping has 44 VSS balls. All 44 real VSS balls must be listed
# as their own rows (VSS_1 .. VSS_44), so we take the FULL VSS pool instead of
# only the 14 rows the main table names.
vss_pool = list(VSS_BALLS)
hva_pool = list(HV_A_BALLS)
hvb_pool = list(HV_B_BALLS)
hva_unresolved = []
for p in pins:
    if p['name'] == 'VSS':
        p['ball'] = vss_pool.pop(0)
    elif p['name'] == 'VDD_HV_A':
        p['ball'] = hva_pool.pop(0) if hva_pool else ''
        if not p['ball']:
            hva_unresolved.append(p['lqfp'])
    elif p['name'] == 'VDD_HV_B':
        p['ball'] = hvb_pool.pop(0)
    else:
        p['ball'] = p['bga']
# The V1.3 main table names only 14 VSS rows, but BGA_mapping has 44 VSS balls.
# Rule "Parsing repeated nets" p.3: list every real ball of the net as its own
# row — synthesize the extra VSS rows from the remaining pool balls.
while vss_pool:
    b = vss_pool.pop(0)
    pins.append({'lqfp': '', 'bga': b, 'ball': b, 'name': 'VSS',
                 'domain': 'PD0', 'type': 'GND', 'default': 'VSS', 'alts': []})
assert not hvb_pool and not vss_pool, (vss_pool, hvb_pool)
print('VSS balls used: all', len(VSS_BALLS), '(BGA has 44 VSS balls, all listed)')
print('VDD_HV_A resolved:', len(HV_A_BALLS), '| unresolved LQFP:', hva_unresolved)

def block_of(p):
    n = p['name']
    if n.startswith('VSS'):
        return 'Ground'
    if n.startswith('VDDA') or n.startswith('VREFH') or n.startswith('VREFL') \
            or n.startswith('V11_') or n.startswith('V15_') or n.startswith('V25') \
            or n in ('VDD_HV_A', 'VDD_HV_B', 'V15_CFG', 'V15_BASE_DRIVER'):
        return 'Power'
    if n == 'OSC32K_XTAL':
        return 'Control'
    if re.fullmatch(r'PT[A-T]\d+', n) or n == 'RESET_B':
        return 'GPIO'
    return 'Other'

ground = [p for p in pins if block_of(p) == 'Ground']
power = [p for p in pins if block_of(p) == 'Power']
gpio = [p for p in pins if block_of(p) == 'GPIO']
# RESET_B (dedicated pin) goes to the PTA bank, appended at the end
reset = [p for p in gpio if p['name'] == 'RESET_B']
gpio = [p for p in gpio if p['name'] != 'RESET_B']
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
    if n == 'RESET_B':
        return 'INPUT'
    if not re.fullmatch(r'PT[A-T]\d+', n):
        return 'PWR'
    return 'BIDIR'

# ---- GPIO: name = pin name + all mux functions separated by '/' ------------
def sort_key(p):
    bank = p['name'][2]
    return (bank, int(p['name'][3:]), p['lqfp'] or '999')

for p in gpio:
    # pin name first, then all mux functions (DEFAULT, ALT0...) in table order
    fns = [p['name']]
    for fn in [p['default']] + list(p['alts']):
        if fn and fn not in fns:
            fns.append(fn)
    p['out'] = '/'.join(fns)

# RESET_B is a dedicated pin — plain name, no mux functions
for p in reset:
    p['out'] = 'RESET_B'
    p['side'] = 'Right'
    p['type'] = 'INPUT'

gpio = sorted(gpio, key=sort_key)

def side_of(p):
    if p in ground or p in power:
        return p['side']
    return 'Right'

# ---- write .xlsx (format per fx3.xlsx reference) ---------------------------
def write_book(path, ball_key, group=False):
    wb2 = openpyxl.Workbook()
    wb2.remove(wb2.active)
    # GPIO split into one sheet per port bank: PTA..PTI
    banks = [b for b in 'ABCDEFGHI'
             if any(p['name'].startswith(f'PT{b}') for p in gpio)]
    sheets = [(f'PT{b}', [p for p in gpio if p['name'].startswith(f'PT{b}')])
              for b in banks]
    # RESET_B appended to the PTA sheet (JTAG bank)
    if reset:
        sheets = [(n, (it + reset) if n == 'PTA' else it) for n, it in sheets]
    # Extra VSS rows (synthesized above from the remaining VSS balls): the V1.3
    # main table names 14 VSS rows but BGA_mapping has 44. Rule "Parsing
    # repeated nets" p.3 lists every real ball, so append them after the table
    # rows. The 14 table rows carry ball == 'VSS' (the net-name column); the
    # synthesized rows carry a real coordinate — select the latter.
    extra_vss = [p for p in pins
                 if p['name'] == 'VSS' and p['ball'] not in VSS_BALLS]
    sheets += [('PWR', power), ('GND', ground)]
    if group:
        sheets = [(n, (it + extra_vss) if n == 'GND' else it)
                  for n, it in sheets]
        # PWR/GND: drop shared-net rows that have no real BGA coordinate
        # (V1.3 main table lists 10 VDD_HV_A rows but BGA_mapping has only 6
        #  real balls — the extra rows are a datasheet inconsistency),
        # then group by base name: groups keep first-appearance order,
        # pins inside a group go by suffix number
        for idx in (1, 2):
            items = [p for p in sheets[idx][1]
                     if not (not p.get('ball') and p['name'] in
                             ('VSS', 'VDD_HV_A', 'VDD_HV_B'))]
            def base_of(name):
                m = re.match(r'^(.*?)_(\d+)$', name)
                return (m.group(1), int(m.group(2))) if m else (name, 0)
            first_seen = {}
            for i, p in enumerate(items):
                b = base_of(p['out'])[0]
                first_seen.setdefault(b, i)
            def sort_key(p):
                b, n = base_of(p['out'])
                return (first_seen[b], b, n)
            sheets[idx] = (sheets[idx][0], sorted(items, key=sort_key))
    for sheet_name, items in sheets:
        sh = wb2.create_sheet(sheet_name)
        for r, p in enumerate(items, start=1):
            sh.cell(row=r, column=1, value=p['out'])
            sh.cell(row=r, column=2, value=p[ball_key] if ball_key in p else p['bga'])
            sh.cell(row=r, column=3, value=type_of(p))
            sh.cell(row=r, column=4, value=side_of(p))
            if p['lqfp']:
                sh.cell(row=r, column=5, value=p['lqfp'])
    wb2.save(path)
    print('WROTE:', path)

# original file fc7300-320-pin.xlsx is kept as-is (ball column with 'VSS' etc.);
# it is often open in Excel, so only the -a1 file is (re)generated here.
DSTA1 = r'D:\work\!myprojects\canfd-logger-fc7300\pinout\fc7300-320-pin-a1.xlsx'
write_book(DSTA1, 'ball', group=True)

# verification
for path in (DSTA1,):
    b2 = openpyxl.load_workbook(path)
    print(path.split('\\')[-1], [(s.title, s.max_row) for s in b2.worksheets])
    for sheet in ('GND', 'PWR'):
        sh = [s for s in b2.worksheets if s.title == sheet][0]
        print('  ===', sheet)
        for row in list(sh.iter_rows(values_only=True))[:8]:
            print('   ', [str(c) if c is not None else '' for c in row])

# rule "Parsing repeated nets" p.4: every Ball matches [A-Z][1-9][0-9]?
# and all balls across all sheets are unique
all_balls = []
for s in b2.worksheets:
    for row in s.iter_rows(values_only=True):
        if row[1]:
            all_balls.append((s.title, str(row[1])))
bad = [b for _, b in all_balls if not re.fullmatch(r'[A-Z][1-9][0-9]?', b)]
dup = {b for _, b in all_balls if sum(1 for x, y in all_balls if y == b) > 1}
assert not bad, ('bad ball cells', bad)
assert not dup, ('duplicate balls', sorted(dup))
print('ball check OK:', len(all_balls), 'cells, all match [A-Z][1-9][0-9]? and unique')

