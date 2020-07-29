#!/bin/sh

python3 -m venv env
./env/bin/pip install --upgrade pip
./env/bin/pip install -r requirements.txt

git clone https://github.com/multiplay/qstat
cd qstat
./autogen.sh
./configure
make

cd ..
mv qstat qstat-1
cp qstat-1/qstat .
rm -rf qstat-1
