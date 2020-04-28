#!/bin/sh
virtualenv -p python2.7 --clear .
env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" ./bin/pip install -r requirements.txt
./bin/buildout $*
echo "run plone with: b5 plone"
