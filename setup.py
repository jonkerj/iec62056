from setuptools import setup, find_packages

long_description = open('README.md', 'r').read()
with open('requirements.txt') as f:
	reqs = f.read().splitlines()

setup(
	author='Jorik Jonker',
	author_email='jorik@kippendief.biz',
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Natural Language :: English',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Software Development :: Libraries',
	],
	description='Library to parse IEC62056/IEC1107/DSMR telegrams',
	include_package_data=True,
	install_requires=reqs,
	long_description=long_description,
	long_description_content_type="text/markdown",
	name='iec62056',
	packages=find_packages(),
	setup_requires=['better-setuptools-git-version'],
	url='https://github.com/jonkerj/iec62056',
	version_config={
		'version_format': '{tag}.dev{sha}',
		'starting_version': '0.1.0',
	},
)
