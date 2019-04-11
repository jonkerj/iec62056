from setuptools import setup, find_packages

long_description = open('README.md', 'r').read()
reqs = [line.strip() for line in open('requirements.txt', 'r') if line and not line.startswith('#')]

setup(
	name='iec62056',
	description='Library to parse IEC62056/IEC1107/DSMR telegrams',
	author='Jorik Jonker',
	author_email='jorik@kippendief.biz',
	url='https://github.com/jonkerj/iec62056',
	version='0.1.7',
	packages=find_packages(),
	package_data={
		'iec62056': ['*.lark'],
	},
	install_requires=reqs,
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: OS Independent',
		'Development Status :: 3 - Alpha',
	],
)
