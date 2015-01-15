import fileinput
import json
import re
import sys

regexp = re.compile('spotify:album:.{22}')

uris = []

for line in fileinput.input():
    uri = regexp.match(line)
    if uri:
        uris.append(uri.group(0))

print json.dumps(uris)
