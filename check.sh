#!/bin/bash

cd `dirname $0`

source ./cc/bin/activate
source ./sendgrid.env

python ./batch.py
