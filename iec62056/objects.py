import time

class Reference(object):
	def __init__(self, i):
		self.id = i
	
	def __repr__(self):
		return '{}-{}:{}.{}.{}'.format(*self.id)
	
	def match(self, other):
		# length mismatch
		if len(other.id) != len(self.id):
			return False
		
		# run every digit
		for digit_self, digit_other in [(str(self.id[i]), str(other.id[i])) for i in range(len(self.id))]:
			# digits don't match directly
			if digit_self != digit_other:
				# if neither is wildcard, mismatch
				if digit_self != '*' and digit_other != '*':
					return False
		return True

class COSEM(object):
	def __init__(self, reference, name):
		self.reference = reference
		self.name = name
	
class Log(COSEM):
	def __init__(self, reference, name, entries):
		super().__init__(reference, name)
		self.entries = entries

	@classmethod
	def factory(cls, reference, entries):
		for r, n, func in cosem_objects:
			if r.match(reference):
				name = n
				return cls(reference, name, entries)
		raise NotImplementedError('OBIS reference {} is not implemented'.format(repr(reference)))
	
	def __repr__(self):
		return '<Log reference={} name={} [{}]>'.format(self.reference, self.name, self.entries)

class Register(COSEM):
	def __init__(self, reference, name, timestamp, value, unit):
		super().__init__(reference, name)
		self.timestamp = timestamp
		self.value = value
		self.unit = unit
	
	@classmethod
	def factory(cls, reference, timestamp, raw, unit):
		for r, n, vcls in cosem_objects:
			if r.match(reference):
				value = vcls(raw)
				name = n
				return cls(reference, name, timestamp, value, unit)
		raise NotImplementedError('OBIS reference {} is not implemented'.format(repr(eeference)))
	
	def __repr__(self):
		if self.timestamp is not None:
			t = time.strftime('%c', self.timestamp)
		else:
			t = None
		return '<Register reference={} name={} timestamp={} value={} unit={}>'.format(self.reference, self.name, t, self.value, self.unit)
	
	def __int__(self):
		return int(self.value)

	def __str__(self):
		return str(self.value)

	def __float__(self):
		return float(self.value)

class Telegram(object):
	def __init__(self, identification, objects, checksum):
		self.vendor, self.version, self.model = identification
		self.objects = objects
		self.checksum = checksum
	
	def  __repr__(self):
		return '<Telegram {}/{} containing {} checksum={}>'.format(self.vendor, self.model, ','.join(self.keys()), self.checksum)
	
	def keys(self):
		return [o.name for o in self.objects]
	
	def __getitem__(self, name):
		for o in self.objects:
			if o.name == name:
				return o
		raise ValueError('key "{}" not in telegram'.format(name))

class Value(object):
	def __init__(self, value):
		self.value = value
	
	def __int__(self):
		raise NotImplementedError('__int__() is not implemented for this value type')
	
	def __float__(self):
		raise NotImplementedError('__float__() is not implemented for this value type')

class IntValue(Value):
	def __init__(self, value):
		self.value = int(value)

	def __int__(self):
		return self.value
	
	def __str__(self):
		return str(self.value)

class FloatValue(Value):
	def __init__(self, value):
		self.value = float(value)

	def __int__(self):
		return self.value
	
	def __str__(self):
		return str(self.value)

class StrValue(Value):
	def __str__(self):
		if self.value is not None:
			return self.value
		else:
			return ''

class TimeValue(Value):
	def __init__(self, value):
		self.value = timestamp(value)

	def __str__(self):
		return time.strftime('%c', self.value)

def timestamp(raw):
	# cosem timestamp format = YYMMDDhhmmssX
	dst = -1
	if len(raw) == 13:
		# the following is borrowed from https://github.com/lvzon/dsmr-p1-parser/blob/master/p1-parser.rl
		if raw[12] == 'S':
			dst = 1
		elif raw[12] == 'W':
			dst = 0
	
	return time.struct_time((
		2000 + int(raw[0:2]), # YY (year)
		int(raw[2:4]),        # MM (mon)
		int(raw[4:6]),        # DD (mday)
		int(raw[6:8]),        # hh (hour)
		int(raw[8:10]),       # mm (min)
		int(raw[10:12]),      # ss (sec)
		0,                    # N/A (wday)
		0,                    # N/A (yday)
		dst,                      # X   (isdst)
		None,                     # N/A (zone)
		None,                     # N/A (gmtoff)
	))

cosem_objects = [
# These are from various DSMR specs
	(Reference((0, 0, 1, 0, 0)),                  'timestamp', TimeValue),
	(Reference((0, 0, 1, 0, 0)),                  'timestamp', TimeValue),
	(Reference((0, 0, 17, 0, 0)),                 'threshold_electricity', FloatValue),
	(Reference((0, 0, 96, 1, 1)),                 'equipment_identifier', StrValue),
	(Reference((0, 0, 96, 3, 10)),                'electricity_switch_position', IntValue),
	(Reference((0, 0, 96, 7, 19)),                'power_failure_duration', IntValue),
	(Reference((0, 0, 96, 7, 21)),                'short_power_failure_count', IntValue),
	(Reference((0, 0, 96, 7, 9)),                 'long_power_failure_count', IntValue),
	(Reference((0, 0, 96, 13, 0)),                'text_message', StrValue),
	(Reference((0, 0, 96, 13, 1)),                'text_message_code', StrValue),
	(Reference((0, 0, 96, 14, 0)),                'electricity_active_tariff', IntValue),
	(Reference((0, '*', 24, 1, 0)),               'device_type', IntValue),
	(Reference((0, '*', 24, 2, 1)),               'gas_delivered', FloatValue),
	(Reference((0, '*', 24, 3, 0)),               'gas_delivered', FloatValue),
	(Reference((0, '*', 24, 4, 0)),               'gas_valve_position', IntValue),
	(Reference((0, '*', 96, 1, 0)),               'equipment_identifier', StrValue),
	(Reference((1, 0, 1, 7, 0)),                  'current_electricity_usage', FloatValue),
	(Reference((1, 0, 1, 8, 1)),                  'electricity_used_tariff_1', FloatValue),
	(Reference((1, 0, 1, 8, 2)),                  'electricity_used_tariff_2', FloatValue),
	(Reference((1, 0, 2, 7, 0)),                  'current_electricity_delivery', FloatValue),
	(Reference((1, 0, 2, 8, 1)),                  'electricity_delivered_tariff_1', FloatValue),
	(Reference((1, 0, 2, 8, 2)),                  'electricity_delivered_tariff_2', FloatValue),
	(Reference((1, 0, 21, 7, 0)),                 'instantaneous_active_power_l1_positive', FloatValue),
	(Reference((1, 0, 22, 7, 0)),                 'instantaneous_active_power_l1_negative', FloatValue),
	(Reference((1, 0, 31, 7, 0)),                 'instantaneous_current_l1', FloatValue),
	(Reference((1, 0, 32, 7, 0)),                 'instantaneous_voltage_l1', FloatValue),
	(Reference((1, 0, 32, 32, 0)),                'voltage_sag_count_l1', IntValue),
	(Reference((1, 0, 32, 36, 0)),                'voltage_swell_count_l1', IntValue),
	(Reference((1, 0, 41, 7, 0)),                 'instantaneous_active_power_l2_positive', FloatValue),
	(Reference((1, 0, 42, 7, 0)),                 'instantaneous_active_power_l2_negative', FloatValue),
	(Reference((1, 0, 51, 7, 0)),                 'instantaneous_current_l2', FloatValue),
	(Reference((1, 0, 52, 7, 0)),                 'instantaneous_voltage_l2', FloatValue),
	(Reference((1, 0, 52, 32, 0)),                'voltage_sag_count_l2', IntValue),
	(Reference((1, 0, 52, 36, 0)),                'voltage_swell_count_l2', IntValue),
	(Reference((1, 0, 61, 7, 0)),                 'instantaneous_active_power_l3_positive', FloatValue),
	(Reference((1, 0, 62, 7, 0)),                 'instantaneous_active_power_l3_negative', FloatValue),
	(Reference((1, 0, 71, 7, 0)),                 'instantaneous_current_l3', FloatValue),
	(Reference((1, 0, 72, 7, 0)),                 'instantaneous_voltage_l3', FloatValue),
	(Reference((1, 0, 72, 32, 0)),                'voltage_sag_count_l3', IntValue),
	(Reference((1, 0, 72, 36, 0)),                'voltage_swell_count_l3', IntValue),
	(Reference((1, 0, 99, 97, 0)),                'power_failure_event_log', None),
	(Reference((1, 3, 0, 2, 8)),                  'version', StrValue),
# These are reverse-engineered Kamstrup multical fields
	(Reference((None, None, 0, 0, None)),         'serial', StrValue),
	(Reference((None, None, 6, 8, None)),         'energy_consumed', FloatValue),
	(Reference((None, None, 6, 26, None)),        'volume_consumed', FloatValue),
	(Reference((None, None, 6, 31, None)),        'operating_hours', IntValue),
]
