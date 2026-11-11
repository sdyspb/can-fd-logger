#!/usr/bin/env python3
"""Build MKDN512GCL-ZC (Nano SD NAND 64 GB, LGA) pinout .xlsx.

Source: hardware/pdf/nand/MKDN512GCL-ZC-C52753986.pdf, p.6
"5 Pin Assignments (SD Mode & SPI Mode)" — top view through package.

Pin numbering (per the package figure, pin-1 marker top-left):
- left side, top->bottom: 1=DAT2, 2=DAT3, 3=CLK, 4=GND
- right side, bottom->top: 5=CMD, 6=DAT0, 7=DAT1, 8=VDD
- duplicates: 9..16 repeat 1..8 (9<->1 ... 16<->8)
- 4 center GND pads are listed as one common TP, pin 17.

Layout rules:
- all interface pins (data + control) are on the LEFT side;
- power has nothing to do with the interface -> RIGHT side, TP included;
- rows are grouped by data (DAT0..DAT3), then control (CLK, CMD), then
  power (VDD, GND, TP); within a signal: main pin then its duplicate.

Naming: *_1 main, *_2 duplicate.
Format follows fc7300-320-pin-a1.xlsx (no header row: Name, Pad, Type, Side).
"""
import openpyxl

DST = r'D:\work\!myprojects\canfd-logger-fc7300\hardware\pinout\MKDN512GCL-ZC Pinout.xlsx'

# Groups: data -> control -> power; each entry (name base, main pin, type, side)
GROUPS = [
    ('DATA', [
        ('DAT0', 6, 'BIDIR', 'LEFT'),
        ('DAT1', 7, 'BIDIR', 'LEFT'),
        ('DAT2', 1, 'BIDIR', 'LEFT'),
        ('DAT3', 2, 'BIDIR', 'LEFT'),
    ]),
    ('CONTROL', [
        ('CLK', 3, 'INPUT', 'LEFT'),
        ('CMD', 5, 'BIDIR', 'LEFT'),
    ]),
    ('POWER', [
        ('VDD', 8, 'PWR', 'RIGHT'),
        ('GND', 4, 'GND', 'RIGHT'),
    ]),
]

wb = openpyxl.Workbook()
wb.remove(wb.active)
ws = wb.create_sheet('Pinout_MKDN512GCL-ZC')
r = 1
for _group, items in GROUPS:
    for base, main, ptype, side in items:
        dup = main + 8  # 9..16, duplicates main pin 1..8
        ws.cell(row=r, column=1, value=f'{base}_1')
        ws.cell(row=r, column=2, value=main)
        ws.cell(row=r, column=3, value=ptype)
        ws.cell(row=r, column=4, value=side)
        r += 1
        ws.cell(row=r, column=1, value=f'{base}_2')
        ws.cell(row=r, column=2, value=dup)
        ws.cell(row=r, column=3, value=ptype)
        ws.cell(row=r, column=4, value=side)
        r += 1
# 4 center GND pads -> one common TP, pin 17 (power side -> RIGHT)
ws.cell(row=r, column=1, value='TP')
ws.cell(row=r, column=2, value=17)
ws.cell(row=r, column=3, value='GND')
ws.cell(row=r, column=4, value='RIGHT')
wb.save(DST)
print('WROTE:', DST)

# verification
b2 = openpyxl.load_workbook(DST)
print([(s.title, s.max_row, s.max_column) for s in b2.worksheets])
rows = list(b2['Pinout_MKDN512GCL-ZC'].iter_rows(values_only=True))
for row in rows:
    print('   ', row)
nums = [row[1] for row in rows]
assert sorted(nums) == list(range(1, 18)), nums
# pairing: every main pin n is directly followed by its duplicate n+8
for i in range(0, 16, 2):
    assert nums[i + 1] == nums[i] + 8, nums[i:i + 2]
assert nums[16] == 17
# figure numbering: left top->bottom 1..4, right bottom->top 5..8
by_name = {row[0]: row[1] for row in rows}
assert by_name['DAT2_1'] == 1 and by_name['DAT3_1'] == 2
assert by_name['CLK_1'] == 3 and by_name['GND_1'] == 4
assert by_name['CMD_1'] == 5 and by_name['DAT0_1'] == 6
assert by_name['DAT1_1'] == 7 and by_name['VDD_1'] == 8
# sides: all interface (data+control) LEFT, all power incl. TP RIGHT
for name, _pin, _t, side in rows:
    if name.startswith(('TP', 'VDD', 'GND')):
        assert side == 'RIGHT', name
    else:
        assert side == 'LEFT', name
print('OK: numbering per figure, paired main/duplicate, '
      'data/control LEFT, power+TP RIGHT')
