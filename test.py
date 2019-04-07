import os
import os.path
import iec62056
import objects

for o in objects.cosem_objects:
	if not len(o) == 3:
		print(o)

p = iec62056.Parser()
for entry in os.listdir('samples'):
	filename = os.path.join('samples', entry)
	if os.path.isfile(filename):
		print('Parsing {}'.format(filename))
		telegram = open(filename, 'rb').read().decode('ascii')
		print(p.parse(telegram))
