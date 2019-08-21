#!/usr/bin/env python

"""
This script takes a JSON dictionary containing traditional chinese characters
as keys, and the simplified equivalents as values. It then outputs a header file
appropriate for inclusion. The header output file contains an array,
`Cn_T2S` which can be used as

```
    simpChr = Cn_T2S[tradChr];
```

the variable Cn_T2S_MinChr contains the smallest key in the dictionary, whereas
Cn_T2S_MaxChr contains the largest key in the dictionary.
"""

import json
import datetime
import sys
from argparse import ArgumentParser

ap = ArgumentParser()
ap.add_argument('-f', '--file', help='Chinese map file', required=True)
ap.add_argument('-o', '--output', help='Where to place the output C source')

options = ap.parse_args()

with open(options.file, 'r') as fp:
    txt = json.load(fp)

if options.output is None or ap.output == '-':
    ofp = sys.stdout
else:
    ofp = open(ap.output, 'w')

CP_MIN = 0xffffffff
CP_MAX = 0x00

for k in txt:
    v = ord(k)
    if v > CP_MAX:
        CP_MAX = v
    if v < CP_MIN:
        CP_MIN = v

ofp.write('''
/**
 * Generated by {script} on {date}
 *
 */
#include <stdint.h>

static const uint16_t Cn_T2S_MinChr = {cp_min};
static const uint16_t Cn_T2S_MaxChr = {cp_max};

static uint16_t Cn_T2S[{cap}]={{
'''.format(
        script=' '.join(sys.argv),
        date=datetime.datetime.now(),
        cp_min=CP_MIN,
        cp_max=CP_MAX,
        cap=CP_MAX+1))




num_items = 0
ITEMS_PER_LINE = 5

for trad, simp in txt.items():
    ix = ord(trad)
    val = ord(simp)
    ofp.write(' [0x{:X}]=0x{:X},'.format(ix, val))
    num_items += 1
    if num_items >= ITEMS_PER_LINE:
        ofp.write('\n')
        num_items = 0

ofp.write('};\n')
ofp.flush()