#!/usr/bin/env python

import IRData.twcr as twcr
import datetime

dte=datetime.datetime(1902,6,1)

#twcr.fetch('observations',dte,version='4.5.1')
#twcr.fetch('prmsl',dte,version='4.5.1')
#twcr.fetch('air.2m',dte,version='4.5.1')

twcr.fetch('observations',dte,version='4.6.1')
twcr.fetch('prmsl',dte,version='4.6.1')
twcr.fetch('air.2m',dte,version='4.6.1')

