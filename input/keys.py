#!/usr/bin/env python3
import sys
import json
from itertools import starmap
from itertools import product
from itertools import chain

def controls(limit=ord(' '), ctloffset=ord('A')-1):
	"""
	# Generate control characters associated with their
	# uppercase relative representation.
	"""
	for i in range(limit):
		ctlchar = chr(ctloffset + i).lower()
		yield ctlchar, i

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
	"""
	# Reorient the keyboard mapping data storing the bindings relative
	# to the modifier set.
	"""
	import collections
	d = collections.defaultdict(list)
	for k, binding in data.items():
		d[tuple(binding[:-1])].append((binding[-1], k))
	return d

def bind(module, modifiers, mapping):
	"""
	# Construct an iterator producing a file image that
	# binds the &modifiers to the keys defined in &mapping using
	# the methods provided by &module.

	# [ Parameters ]
	# /module/
		# The primitives used to format the lines that make up the bindings.
	# /modifiers/
		# The combinations of modifiers to bind. Normally `list(range(1, 9))`.

		# Modifiers are represented using the exact decimals used by
		# the transmitted sequences, which are bitmaps of modifiers.
		# First bit represents `shift`. Second, `alt`. And third, `control`.
	# /mapping/
		# The high level keyboard mapping defining the alphabet and symbols
		# of the system's keyboard.
	"""
	shifts = mapping.pop(('shift',))
	metas = mapping.pop(('shift', 'meta',))

	# Number of combinations being expanded here.
	return map(module.encode, chain(
		# Bind shift-meta modified bindings.
		starmap(module.custom, product([(7 ^ (1 << 2)) + 1], metas)),

		# Control characters.
		starmap(module.control, product([(1 << 2) + 1], controls())),

		# Special case &exceptions, unmodified with direct writes.
		starmap(module.insert, product([1], exceptions)),
		# When modified, CSI-u encoded.
		starmap(module.csi_u, product(modifiers, exceptions)),

		# Lower case.
		starmap(module.insert, product([1], (ord(k[0]) for k in shifts))),
		# Upper case.
		starmap(module.insert, product(modifiers[:2], (ord(k[1]) for k in shifts))),
		# Modifier combinations of the configured alphabet.
		starmap(module.csi_u, product(modifiers[2:], (ord(k[0]) for k in shifts))),

		# Modifier combinations of Insert, Page Up, and Page Down.
		starmap(module.tilde, product(modifiers, [
			(2, "Insert"),
			(5, "Prior"),
			(6, "Next"),

			# Does not appear to be the preferred mapping on macOS.
			#(7, "Home"),
			#(8, "End"),
		])),

		# Traditional F-Keys. Minding the gap.
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
