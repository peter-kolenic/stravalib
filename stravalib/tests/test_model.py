from __future__ import absolute_import, unicode_literals

from stravalib import model
from stravalib import unithelper as uh
from stravalib.tests import TestBase
from units.quantity import Quantity


class ModelTest(TestBase):

    def setUp(self):
        super(ModelTest, self).setUp()

    def test_entity_collections(self):

        a = model.Athlete()
        d = {'clubs': [{'resource_state': 2, 'id': 7, 'name': 'Team Roaring Mouse'},
                       {'resource_state': 2, 'id': 1, 'name': 'Team Strava Cycling'},
                       {'resource_state': 2, 'id': 34444, 'name': 'Team Strava Cyclocross'}]
             }
        a.from_dict(d)

        self.assertEquals(3, len(a.clubs))
        self.assertEquals('Team Roaring Mouse', a.clubs[0].name)

    def test_speed_units(self):
        a = model.Activity()

        a.max_speed = 1000  # m/s
        a.average_speed = 1000  # m/s
        self.assertEquals(3600.0, float(uh.kph(a.max_speed)))
        self.assertEquals(3600.0, float(uh.kph(a.average_speed)))

        a.max_speed = uh.mph(1.0)
        #print repr(a.max_speed)

        self.assertAlmostEqual(1.61, float(uh.kph(a.max_speed)), places=2)

    def test_time_intervals(self):
        segment = model.Segment()
        # s.pr_time = XXXX

        split = model.Split()
        split.moving_time = 3.1
        split.elapsed_time = 5.73

    def test_distance_units(self):

        # Gear
        g = model.Gear()
        g.distance = 1000
        self.assertEquals(1.0, float(uh.kilometers(g.distance)))

        # Metric Split
        split = model.Split()
        split.distance = 1000  # meters
        split.elevation_difference = 1000  # meters
        self.assertIsInstance(split.distance, Quantity)
        self.assertIsInstance(split.elevation_difference, Quantity)
        self.assertEquals(1.0, float(uh.kilometers(split.distance)))
        self.assertEquals(1.0, float(uh.kilometers(split.elevation_difference)))
        split = None

        # Segment
        s = model.Segment()
        s.distance = 1000
        s.elevation_high = 2000
        s.elevation_low = 1000
        s.pr_distance = 1000
        self.assertIsInstance(s.distance, Quantity)
        self.assertIsInstance(s.elevation_high, Quantity)
        self.assertIsInstance(s.elevation_low, Quantity)
        self.assertEquals(1.0, float(uh.kilometers(s.distance)))
        self.assertEquals(2.0, float(uh.kilometers(s.elevation_high)))
        self.assertEquals(1.0, float(uh.kilometers(s.elevation_low)))
        self.assertEquals(1.0, float(uh.kilometers(s.pr_distance)))

        # Activity
        a = model.Activity()
        a.distance = 1000  # m
        a.total_elevation_gain = 1000  # m
        self.assertIsInstance(a.distance, Quantity)
        self.assertIsInstance(a.total_elevation_gain, Quantity)
        self.assertEquals(1.0, float(uh.kilometers(a.distance)))
        self.assertEquals(1.0, float(uh.kilometers(a.total_elevation_gain)))

    def test_weight_units(self):
        """
        """
        # PowerActivityZone
