import setuptools
from setuptools import setup

setup(
    name="snake-tail",
    version="1.0.1",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[
        "clint",
        "requests"
    ],

    entry_points={
        "console_scripts": [
            'snake-tail = snake_tail.snake_tail:main'
        ]
    },

    include_package_data=True,
    zip_safe=False,

    author="Alex Kornitzer",
    author_email="alex.kornitzer@countercept.com",
    description="The command line ui for snake",
    license="https://github.com/countercept/snake-tail/blob/master/LICENSE",
    url="https://github.com/countercept/snake-tail",
)
