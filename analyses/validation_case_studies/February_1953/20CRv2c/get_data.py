import Meteorographica.data.twcr as twcr
twcr.fetch('prmsl',1953,version='2c')
twcr.fetch_observations(1953,version='2c')
