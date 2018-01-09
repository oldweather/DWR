# (C) British Crown Copyright 2017, Met Office
#
# This code is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
"""
Test cases for Daily Weather Report module.

"""

import os
import unittest
import DWR
 
class TestUM(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_get_data_dir(self):
        scratch=os.getenv('SCRATCH')
        del os.environ['SCRATCH']
        with self.assertRaises(StandardError) as cm:
            DWR.get_data_dir()
        self.assertIn('SCRATCH environment variable is undefined',
                      cm.exception)
        os.environ['SCRATCH']=scratch
        
if __name__ == '__main__':
    unittest.main()
