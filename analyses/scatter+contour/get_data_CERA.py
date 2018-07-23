#!/usr/bin/env python

import IRData.cera20c as cera20c
import datetime

dte=datetime.datetime(1901,1,1)
cera20c.fetch('prmsl',dte)
