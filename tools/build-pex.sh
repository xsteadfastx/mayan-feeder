#!/bin/bash

set -e

pex -r <(pipenv lock -r | cut -d' ' -f1) . -e mayan_feeder.cli:main -o dist/mayanfeeder-`uname -s`-`uname -m`.pex -v
