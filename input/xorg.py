"""
# X.org keyboard information tables for use with xterm translations.
"""

_key_identifiers = {
	"!": "exclam",
	"@": "at",
	"#": "numbersign",
	"$": "dollar",
	"%": "percent",
	"^": "asciicircum",
	"&": "ampersand",
	"*": "asterisk",
	"(": "parenleft",
	")": "parenright",
	"`": "grave",
	"~": "asciitilde",
	"-": "minus",
	"_": "underscore",
	"=": "equal",
	"+": "plus",
	"[": "bracketleft",
	"{": "braceleft",
	"]": "bracketright",
	"}": "braceright",
	"\\": "backslash",
	"|": "bar",
	";": "semicolon",
	":": "colon",
	"'": "apostrophe",
	'"': "quotedbl",
	",": "comma",
	"<": "less",
	".": "period",
	">": "greater",
	"/": "slash",
	"?": "question",

	"\x7F": "Delete",
	"\x1B": "Escape",
	"\x08": "BackSpace",
	"\x09": "Tab",
	"\x0D": "Return",
	"\x20": "space",
}

_key_identifiers.update({
	f"[F-{i}]": "F" + str(i) for i in range(1, 16)
})

def kid(key):
	return _key_identifiers.get(key, key)

def modified(bits, field):
	if bits & field:
		return ''
	else:
		return '~'

def xterm_modifiers(mods):
	return ' '.join([
		modified(mods, 1) + 'Shift',
		modified(mods, 2) + 'Alt',
		modified(mods, 4) + 'Ctrl',
	])

arrow_map = {
	'Up': 'A',
	'Down': 'B',
	'Right': 'C',
	'Left': 'D',
	'Home': 'H',
	'End': 'F',
}

def arrow(modifiers, key):
	if modifiers > 1:
		stroke = f'string("[1;{modifiers}{arrow_map[key]}")'
	else:
		# For arrows, applications may not recognize/ignore modifiers.
		stroke = f'string("[{arrow_map[key]}")'
	mods = xterm_modifiers(modifiers-1)
	return mods + ' <Key>' + key + ': string(0x1b) ' + stroke

def tilde(modifiers, key, *, terminator='~'):
	cid, kid = key
	if modifiers > 1:
		stroke = f'string("[{cid};{modifiers}{terminator}")'
	else:
		# Like arrows, applications may not recognize/ignore modifiers.
		stroke = f'string("[{cid}{terminator}")'
	mods = xterm_modifiers(modifiers-1)
	return mods + ' <Key>' + kid + ': string(0x1b) ' + stroke

def csi_u(modifiers, key, *, terminator='u'):
	ki = chr(key)
	stroke = f'string("[{key};{modifiers}{terminator}")'
	mods = xterm_modifiers(modifiers-1)
	return mods + ' <Key>' + kid(ki) + ': string(0x1b) ' + stroke

def insert(modifiers, key, *, terminator='u'):
	ki = chr(key)
	h = hex(key)
	stroke = f'string({h})'
	mods = xterm_modifiers(modifiers-1)
	return mods + ' <Key>' + kid(ki) + ': ' + stroke

def custom(modifiers, rekey):
	ki, custom = rekey
	stroke = f'string({custom})'
	mods = xterm_modifiers(modifiers-1)
	return mods + ' <Key>' + kid(ki) + ': ' + stroke

def ctlkeys(limit=ord(' '), ctloffset=ord('A')-1):
	for i in range(limit):
		ctlchar = chr(ctloffset + i).lower()
		if ctlchar in _key_identifiers:
			k = _key_identifiers[ctlchar]
		else:
			k = ctlchar
		yield (f'~Shift ~Alt Ctrl <Key>{k}: string({hex(i)})')

def encode(line):
	return line + ' \\n\\\n'
