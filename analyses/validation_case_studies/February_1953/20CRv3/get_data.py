import Meteorographica.data.twcr as twcr
twcr.fetch('prmsl',1953,2,version='4.5.1')
twcr.fetch_observations(1953,2,version='4.5.1')
