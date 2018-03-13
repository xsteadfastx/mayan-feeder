"""Setup."""

from setuptools import setup

NAME = 'mayan_feeder'
VERSION = '0.0.0'
URL = 'https://github.com/xsteadfastx/mayan-feeder'
AUTHOR = 'Marvin Steadfast'
AUTHOR_EMAIL = 'marvin@xsteadfastx.org'

REQUIRES = [
    'click',
    'flask',
    'flask-bootstrap',
    'flask-socketio',
    'flask-wtf',
    'pillow',
    'pyyaml',
    'requests',
    'typing',
]


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='MIT',
    url=URL,
    package_dir={'': 'src'},
    packages=['mayan_feeder'],
    include_package_data=True,
    # install_requires=REQUIRES,
    entry_points={
        'console_scripts': [
            'mayanfeeder=mayan_feeder.cli:cli'
        ]
    }
)
