import os

from setuptools import setup, find_packages

install_requires = [
    "aiohttp>=3.8.4",
    "gql>=3.4",
]

setup(
    name="monarchmoney",
    version="1.0",
    description="Monarch Money API for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hammem/monarchmoney",
    author="hammem",
    author_email="hammem@users.noreply.github.com",
    license="MIT",
    classifiers=[],
    keywords="monarch money, financial, money, personal finance",
    install_requires=install_requires,
    include_package_data=True,
    zip_safe=False,
    platforms="any",
)
