import time

def p1version(raw):
	if raw=='42':
		return '4.2'
	if raw=='50':
		return '5.0'
	raise NotImplementedError('P1 version {} is not implemented'.format(raw))

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
