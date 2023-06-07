"""
# Rust keyboard information tables, primarily for use with Alacritty.
"""

_key_identifiers = {
	"!": "Exclamation",
	"@": "At",
	"#": "NumberSign",
	"$": "DollarSign",
	"%": "Percent",
	"^": "Caret",
	"&": "Ampersand",
	"*": "Multiply",
	"(": "LParen",
	")": "RParen",
	"`": "Grave",
	"~": "Tilde",
	"-": "Minus",
	"_": "Underline",
	"=": "Equals",
	"+": "Add",
	"[": "LBracket",
	"]": "RBracket",
	"{": "LBrace",
	"}": "RBrace",
	"\\": "Backslash",
	"|": "bar",
	";": "Semicolon",
	":": "Colon",
	"'": "Apostrophe",
	'"': "quotedbl",
	",": "Comma",
	"<": "LessThan",
	".": "Period",
	">": "GreaterThan",
	"/": "Slash",
	"?": "QuestionMark",

	"\x7F": "Delete",
	"\x1B": "Escape",
	"\x08": "Back",
	"\x09": "Tab",
	"\x0D": "Return",
	"\x20": "Space",

	"0": "Key0",
	"1": "Key1",
	"2": "Key2",
	"3": "Key3",
	"4": "Key4",
	"5": "Key5",
	"6": "Key6",
	"7": "Key7",
	"8": "Key8",
	"9": "Key9",

}
_key_identifiers.update({
	f"[F-{i}]": "F" + str(i) for i in range(1, 16)
})

def kid(key):
	return _key_identifiers.get(key, key)
