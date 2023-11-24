from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ksa/__init__.py
from ksa import __version__ as version

setup(
	name="ksa",
	version=version,
	description="KSA VAT settings for Saudi Arabia",
	author="ERPGulf https://www.ERPGulf.com Courtesy: forked from AhmadPak & 8848Digital",
	author_email="support@ERPGulf.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
