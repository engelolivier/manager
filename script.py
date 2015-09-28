#!/usr/bin/env python3
# coding: utf-8

import requests


data = {}
data['name']="Changer de password"
data['date_start']="2015-01-01 00:00:00"
data['date_end']="2015-01-03 00:00:00"


headers = {'Authorization': 'Token f5e2d3870b4e8bea94684649a4e52df0d754c323'}

r = requests.post('http://localhost:8000/api/task/', headers=headers, data=data)
print(r.text)
