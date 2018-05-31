import unittest
import DIYA
import pandas

test_obs = pandas.DataFrame({'latitude' :[51.51,52.49,50.72,51.75,55.76],
                             'longitude':[-0.13,-1.89,-3.53,-1.26,37.62],
                             'value'    :[1001.0,1100.3,23.6,1030.0,998.2],
                             'name'     :['LONDON','BIRMINGHAM',
                                          'EXETER','OXFORD',
                                          'MOSCOW']})
 
class Distance(unittest.TestCase):
 
    def test_distance_london_exeter(self):
        self.assertAlmostEqual(DIYA.haversine(test_obs.iloc[0],
                                              test_obs.iloc[2]),
                               253,places=0)

    def test_distance_london_moscow(self):
        self.assertAlmostEqual(DIYA.haversine(test_obs.iloc[0],
                                              test_obs.iloc[4]),
                               2501,places=0)

    def test_stations_within_500km_of_london(self):
        self.assertEqual(list(DIYA.nearby_observations(test_obs.iloc[[1,2,3,4]],
                                                  test_obs.iloc[0],500).name),
                              ['BIRMINGHAM','EXETER','OXFORD'])

    def test_stations_within_5km_of_london(self):
        self.assertTrue(DIYA.nearby_observations(test_obs.iloc[[1,2,3,4]],
                                                 test_obs.iloc[0],5).empty)

  
if __name__ == '__main__':
    unittest.main()
