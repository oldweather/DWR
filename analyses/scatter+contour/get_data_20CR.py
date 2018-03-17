import Meteorographica.data.twcr as twcr
twcr.fetch('prmsl',1901,version='2c')
twcr.fetch_observations(1901,version='2c')
