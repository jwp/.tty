#!/usr/bin/env python3
import sys
import json
from itertools import starmap
from itertools import product
from itertools import chain

exceptions = [
	0x7f, # "delete"
	0x1b, # escape
	0x08, # backspace
	0x09, # tab
	0x0d, # return
	0x20, # space
]

navigation = {
	'Up': 'A',
	'Down': 'B',
	'Right': 'C',
	'Left': 'D',
	'Home': 'H',
	'End': 'F',
}

def demap(data):
	import collections
	d = collections.defaultdict(list)
	for k, binding in data.items():
		d[tuple(binding[:-1])].append((binding[-1], k))
	return d

def bind(module, modifiers, mapping):
	shifts = mapping.pop(('shift',))
	metas = mapping.pop(('shift', 'meta',))

	return map(module.encode, chain(
		starmap(module.custom, product([(7 ^ (1 << 2))+1], metas)),
		# Low-ASCII.
		module.ctlkeys(),
		starmap(module.insert, product([1], exceptions)),
		starmap(module.csi_u, product(modifiers, exceptions)),

		# Alphabet and usual symbols.
		starmap(module.insert, product([1], (ord(k[0]) for k in shifts))),
		starmap(module.insert, product(modifiers[:2], (ord(k[1]) for k in shifts))),
		starmap(module.csi_u, product(modifiers[2:], (ord(k[0]) for k in shifts))),

		starmap(module.tilde, product(modifiers, [
			(2, "Insert"),
			(5, "Prior"),
			(6, "Next"),

			# Does not appear to be the preferred mapping on macOS.
			#(7, "Home"),
			#(8, "End"),
		])),

		# Traditional F-Keys.
		starmap(module.tilde, product(modifiers, [
			(10 + i, "F" + str(i)) for i in range(1, 6)
		])),
		starmap(module.tilde, product(modifiers, [
			(11 + i, "F" + str(i)) for i in range(6, 11)
		])),
		starmap(module.tilde, product(modifiers, [
			(12 + i, "F" + str(i)) for i in range(11, 13)
		])),

		# Traditional CSI arrows, home, and end.
		starmap(module.arrow, product(modifiers, navigation.items())),
	))

import xorg
with open(sys.argv[1]) as f: # Keyboard mapping.
	kbmap = json.load(f)
sys.stdout.writelines(bind(xorg, list(range(1, 9)), demap(kbmap)))
