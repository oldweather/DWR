import Meteorographica.data.twcr as twcr
twcr.fetch('prmsl',1903,10,version='4.5.1')
twcr.fetch_observations(1903,10,version='4.5.1')
