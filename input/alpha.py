#!/usr/bin/env python3
# English alphabet description for generating bindings.
import sys
import json

data = {
	k.upper(): ['shift', k]
	for k in map(chr, range(ord('a'), ord('z')+1))
}
for path in sys.argv[1:]:
	with open(path, 'r') as f:
		data.update(json.load(f))

data.pop('', None)
json.dump(data, sys.stdout)
