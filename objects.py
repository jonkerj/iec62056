import time
import parsers

cosem_objects = [
# These are from various DSMR specs
	('0-0:1.0.0',   'timestamp', parsers.timestamp),
	('0-0:1.0.0',   'timestamp', parsers.timestamp),
	('0-0:17.0.0',  'threshold_electricity', float),
	('0-0:96.1.1',  'equipment_identifier', str),
	('0-0:96.3.10', 'electricity_switch_position', int),
	('0-0:96.7.19', 'power_failure_duration', int),
	('0-0:96.7.21', 'short_power_failure_count', int),
	('0-0:96.7.9',  'long_power_failure_count', int),
	('0-0:96.13.0', 'text_message', str),
	('0-0:96.13.1', 'text_message_code', str),
	('0-0:96.14.0', 'electricity_active_tariff', int),
	('0-1:24.1.0',  'device_type', int),
	('0-1:24.2.1',  'gas_delivered', float),
	('0-1:24.3.0',  'gas_delivered', float),
	('0-1:24.4.0',  'gas_valve_position', int),
	('0-1:96.1.0',  'equipment_identifier', str),
	('0-2:24.1.0',  'device_type', int),
	('0-2:24.4.0',  'gas_valve_position', int),
	('0-2:96.1.0',  'equipment_identifier', str),
	('1-0:1.7.0',   'current_electricity_usage', float),
	('1-0:1.8.1',   'electricity_used_tariff_1', float),
	('1-0:1.8.2',   'electricity_used_tariff_2', float),
	('1-0:2.7.0',   'current_electricity_delivery', float),
	('1-0:2.8.1',   'electricity_delivered_tariff_1', float),
	('1-0:2.8.2',   'electricity_delivered_tariff_2', float),
	('1-0:21.7.0',  'instantaneous_active_power_l1_positive', float),
	('1-0:22.7.0',  'instantaneous_active_power_l1_negative', float),
	('1-0:31.7.0',  'instantaneous_current_l1', float),
	('1-0:32.7.0',  'instantaneous_voltage_l1', float),
	('1-0:32.32.0', 'voltage_sag_count_l1', int),
	('1-0:32.36.0', 'voltage_swell_count_l1', int),
	('1-0:41.7.0',  'instantaneous_active_power_l2_positive', float),
	('1-0:42.7.0',  'instantaneous_active_power_l2_negative', float),
	('1-0:51.7.0',  'instantaneous_current_l2', float),
	('1-0:52.7.0',  'instantaneous_voltage_l2', float),
	('1-0:52.32.0', 'voltage_sag_count_l2', int),
	('1-0:52.36.0', 'voltage_swell_count_l2', int),
	('1-0:61.7.0',  'instantaneous_active_power_l3_positive', float),
	('1-0:62.7.0',  'instantaneous_active_power_l3_negative', float),
	('1-0:71.7.0',  'instantaneous_current_l3', float),
	('1-0:72.7.0',  'instantaneous_voltage_l3', float),
	('1-0:72.32.0', 'voltage_sag_count_l3', int),
	('1-0:72.36.0', 'voltage_swell_count_l3', int),
	('1-0:99.97.0', 'power_failure_event_log', None),
	('1-3:0.2.8',   'version', parsers.p1version),
# These are reverse-engineered Kamstrup multical fields
	('0.0',         'serial', str),
	('6.8',         'energy_consumed', float),
	('6.26',        'volume_consumed', float),
	('6.31',        'operating_hours', int),
]

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
			if r == reference:
				name = n
				return cls(reference, name, entries)
		raise NotImplementedError('OBIS reference {} is not implemented'.format(reference))
	
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
		for r, n, func in cosem_objects:
			if r == reference:
				value = func(raw)
				name = n
				return cls(reference, name, timestamp, value, unit)
		raise NotImplementedError('OBIS reference {} is not implemented'.format(reference))
	
	def __repr__(self):
		if self.timestamp is not None:
			t = time.strftime('%c', self.timestamp)
		else:
			t = None
		return '<Register reference={} name={} timestamp={} value={} unit={}>'.format(self.reference, self.name, t, self.value, self.unit)

class Telegram(object):
	def __init__(self, identification, objects, checksum):
		self.vendor, self.version, self.model = identification
		self.objects = objects
		self.checksum = checksum
	
	def  __repr__(self):
		return '<Telegram {}/{} containing {} checksum={}>'.format(self.vendor, self.model, ','.join(self.keys()), self.checksum)
	
	def keys(self):
		return [o.name for o in self.objects]
