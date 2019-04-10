import os
import os.path
import iec62056.parser
import iec62056.objects

p = iec62056.parser.Parser()
for entry in os.listdir('samples'):
	filename = os.path.join('samples', entry)
	if os.path.isfile(filename):
		print('Parsing {}'.format(filename))
		telegram = open(filename, 'rb').read().decode('ascii')
		t = p.parse(telegram)
		for k in t.keys():
			o = t[k]
			if isinstance(o, iec62056.objects.Register):
				print('  {} = {}'.format(k, o.value))
