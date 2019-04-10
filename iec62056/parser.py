import logging
import os
import os.path
from lark import Lark, Transformer
import iec62056.objects

class IECTransformer(Transformer):
	def vendor(self, tree):
		return ''.join(tree)
	
	def model(self, tree):
		return ''.join(tree)
	
	def version(self, tree):
		if len(tree) > 0:
			return str(tree[0])
		else:
			return None
	
	def header_iec(self, tree):
		return (tree[0], tree[1], tree[2])
	
	def header_dsmr(self, tree):
		return (tree[0], tree[1], tree[2])
	
	def footer_iec(self, tree):
		return tree[0]
	
	def footer_dsmr(self, tree):
		if len(tree) > 0:
			return tree[0]
		else:
			return None
	
	def checksum1(self, tree):
		return ord(tree[0][0])
	
	def checksum4(self, tree):
		h = ''.join(tree[0:4])
		return int(h, 16)
	
	def id_abcde(self, tree):
		return iec62056.objects.Reference(tuple(map(int, tree)))

	def id_cd(self, tree):
		return iec62056.objects.Reference((None, None, int(tree[0]), int(tree[1]), None))
	
	def value(self, tree):
		return str(tree[0])
	
	def unit(self, tree):
		return str(tree[0])
	
	def cosem_value_unit(self, tree):
		return (tree[0], tree[1])
	
	def cosem_value(self, tree):
		return (tree[0], None)
	
	def cosem_empty(self, tree):
		return (None, None)
	
	def timestamp(self, tree):
		# cosem timestamp format = YYMMDDhhmmssX
		# tree[0] = YYMMDDhhmmss
		# tree[1] = X (DST)
		if len(tree) == 2:
			return iec62056.objects.timestamp(tree[0] + tree[1])
		else:
			return iec62056.objects.timestamp(tree[0])
	
	def register(self, tree):
		reference, (value, unit) = tree
		return iec62056.objects.Register.factory(reference, None, value, unit)
	
	def mbus(self, tree):
		return (tree[0], tree[1])
	
	def timestamp_register(self, tree):
		reference, (timestamp, (value, unit)) = tree
		return iec62056.objects.Register.factory(reference, timestamp, value, unit)
	
	def logentry(self, tree):
		return (tree[0], tree[1][0], tree[1][1])

	def profilegeneric(self, tree):
		n = int(tree.pop(0))
		reference = tree.pop(0)
		entries = tree
		assert len(entries) == n
		return [iec62056.objects.Register.factory(reference, timestamp, value, unit) for timestamp, value, unit in entries]
	
	def log(self, tree):
		reference = tree.pop(0)
		entries = tree
		return iec62056.objects.Log.factory(reference, entries)
	
	def dsmr3_gas(self, tree):
		return (tree[0], tree[4], tree[5], tree[6])
	
	def dsmr3_gas_register(self, tree):
		register, (timestamp, reg, unit, value) = tree
		return iec62056.objects.Register.factory(reg, timestamp, value, unit)
	
	def objects(self, tree):
		return tree
	
	def telegram(self, tree):
		return iec62056.objects.Telegram(tree[0], tree[1], tree[2])

class Parser(object):
	def __init__(self):
		this_dir, this_filename = os.path.split(__file__)
		grammar_file = os.path.join(this_dir, 'grammar.lark')
		self.parser = Lark.open(grammar_file, start='telegram')
		self.transformer = IECTransformer()
	
	def parse(self, data):
		tree = self.parser.parse(data)
		return self.transformer.transform(tree)
