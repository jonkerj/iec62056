# iec62056
a robust IEC1107/IEC62056 parser in Python.

This library is meant to parse IEC1107/IEC62056 telegrams in Python. You'll need
this to process information from your smart meter (e.g. DSMR P1). The code
differs from other libraries in several ways:

* It actually parses the messages using a (EBNF) grammar. This makes the parsing
  robust and extendable.
* It is designed as an external library instead of being inseperable with other
  software components (such as P1 serial readers).
* It aims to handle all IEC 62056 formatted telegrams, not only DSMR. I needed
  this, because of my IEC 1107 speaking district heat meter, which resembles
  DSMR.

# Compatibility
This module is targeted to be compatible with all kinds of digital meters
outputting IEC62056 formatted telegrams. It implements several (sub)standards.

## Standards
The module implements the following standards:

* IEC 1107/IEC 62056-21 (COSEM, OBIS). IEC 1107 was superseded by IEC 62056
* DSMR (versions 2.2, 4.0, 4.0.5, 4.0.7, 4.2, 5.0)

## Data types
These data types are recognised:

* Standard COSEM OBIS register
* COSEM OBIS timestamped register (e.g. gas via M-Bus)
* Profile Generic (e.g. power failure logs)

## Equipment
Testing was done with sample telegrams from the following meters:

* Kamstrup Multical 66C (district heating meter)
* Kaifa MA 105
* Iskra AM 550
* Iskra MT 382
* Landis + Gyr E350/ZCF110
* ZIV 5CTA3 (aka Enexis ESMR5)

# Usage

```python
$ pip install iec62056
$ python3
>>> import iec62056
>>> p = iec62056.parser.Parser()
>>> t = p.parse(b'... your telegram ')
>>> print(t.keys())
>>> for k in t.keys():
...   o = t[k]
...   if isinstance(o, iec62056.objects.Register):
...     print('  {} = {}'.format(k, o.value))
>>>
```

# Thanks
Since specs on IEC 62056/1107 and DSMR can sometimes be tough to find or
interpret, I used a lot of concepts from other projects. I've used knowledge
from these projects:

* Nigel Dokter's [dsmr_parser](https://github.com/ndokter/dsmr_parser)
* Matthijs Kooiman's [arduino-dsmr](https://github.com/matthijskooijman/arduino-dsmr)
* Levien van Zon's [dsmr-p1-parser](https://github.com/lvzon/dsmr-p1-parser)
* [OpenHAB addon repository](https://github.com/openhab/openhab2-addons)
