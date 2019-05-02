import os
import os.path
import iec62056.parser
import iec62056.objects
import iec62056.samples

p = iec62056.parser.Parser()
for name, telegram in iec62056.samples.ALL:
	print(f'Parsing {name}')
	t = p.parse(telegram.decode('ascii'))
	for k in t.keys():
		o = t[k]
		if isinstance(o, iec62056.objects.Register):
			print('  {} = {}'.format(k, o.value))
