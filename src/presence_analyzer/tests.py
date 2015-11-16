# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
from __future__ import unicode_literals

import os.path
import json
import datetime
import unittest

from presence_analyzer import main, views, utils


TEST_DATA_CSV = os.path.join(
    os.path.dirname(__file__), '..', '..', 'runtime', 'data', 'test_data.csv'
)


# pylint: disable=maybe-no-member, too-many-public-methods
class PresenceAnalyzerViewsTestCase(unittest.TestCase):
    """
    Views tests.
    """
    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})
        self.client = main.app.test_client()

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_mainpage(self):
        """
        Test main page redirect.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 302)
        assert resp.headers['Location'].endswith('/presence_weekday.html')

    def test_api_users(self):
        """
        Test users listing.
        """
        resp = self.client.get('/api/v1/users')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content_type, 'application/json')
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        self.assertDictEqual(data[0], {'user_id': 10, 'name': 'User 10'})

    def test_mean_time_weekday_view(self):
        mean_time_data = self.client.get('/api/v1/mean_time_weekday/10')
        self.assertEqual(mean_time_data.content_type, 'application/json')
        self.assertEqual(mean_time_data.status_code, 200)
        data = json.loads(mean_time_data.data)
        self.assertItemsEqual(data,  [
            ['Mon', 0],
            ['Tue', 30047.0],
            ['Wed', 24465.0],
            ['Thu', 23705.0],
            ['Fri', 0],
            ['Sat', 0],
            ['Sun', 0],
        ])
        dataget = views.get_data()
        self.assertIsInstance(dataget, dict)
        sample_date = datetime.date(2013, 9, 10)
        self.assertItemsEqual(
            dataget[10][sample_date].keys(),
            ['start', 'end']
        )

    def test_mean_time_weekday_view_404(self):
        mean_time_data = self.client.get('/api/v1/presence_weekday/9')
        self.assertEqual(mean_time_data.status_code, 404)

    def test_presence_weekday_view(self):
        presence_data = self.client.get('/api/v1/presence_weekday/10')
        self.assertEqual(presence_data.content_type, 'application/json')
        self.assertEqual(presence_data.status_code, 200)
        data = json.loads(presence_data.data)
        self.assertItemsEqual(data, [
            ['Weekday', 'Presence (s)'],
            ['Mon', 0],
            ['Tue', 30047],
            ['Wed', 24465],
            ['Thu', 23705],
            ['Fri', 0],
            ['Sat', 0],
            ['Sun', 0],
        ])

    def test_presence_weekday_view_404(self):
        presence_data = self.client.get('/api/v1/presence_weekday/9')
        self.assertEqual(presence_data.status_code, 404)

    def test_mean_time_weekday_view(self):
        mean_time_url = '/api/v1/mean_time_weekday/<int:user_id>'
        mean_time_data = self.client.get(mean_time_url)
        self.assertEqual(mean_time_data.content_type, 'text/html')

        # 404 status code case
        self.assertTrue(mean_time_data)
        self.assertEqual(mean_time_data.status_code, 404,
                         'Invalid status code value received.')
        # 200 status code case
        mean_time_data = views.presence_weekday_view(11)
        self.assertTrue(mean_time_data)
        self.assertEqual(mean_time_data.status_code, 200)

    def test_presence_weekday_view(self):
        presence_url = '/api/v1/presence_weekday/<int:user_id>'
        presence_data = self.client.get(presence_url)
        self.assertEqual(presence_data.content_type, 'text/html')

        # 404 status code case
        self.assertTrue(presence_data)
        self.assertEqual(presence_data.status_code, 404,
                         'Invalid status code value received.')
        # 200 status code case
        presence_data = views.presence_weekday_view(11)
        self.assertTrue(presence_data)
        self.assertEqual(presence_data.status_code, 200)


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """
    Utility functions tests.
    """

    def setUp(self):
        """
        Before each test, set up a environment.
        """
        main.app.config.update({'DATA_CSV': TEST_DATA_CSV})

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        pass

    def test_get_data(self):
        """
        Test parsing of CSV file.
        """
        data = utils.get_data()
        self.assertIsInstance(data, dict)
        self.assertItemsEqual(data.keys(), [10, 11])
        sample_date = datetime.date(2013, 9, 10)
        self.assertIn(sample_date, data[10])
        self.assertItemsEqual(data[10][sample_date].keys(), ['start', 'end'])
        self.assertEqual(
            data[10][sample_date]['start'],
            datetime.time(9, 39, 5)
        )

    def test_group_by_weekday(self):
<<<<<<< HEAD
        group_data = utils.group_by_weekday(
            {datetime.date(2012, 11, 20):
                {'end': datetime.time(17, 0, 42),
                 'start': datetime.time(8, 19, 37)}}
        )
        self.assertIsInstance(group_data, list)
        self.assertIsNotNone(group_data)
        self.assertIn(group_data[1] or group_data[2] or group_data[3],
                      [[x] for x in range(31265, 31280)])
        self.assertEqual(
            len(group_data), 7
=======
        sample_data = utils.get_data()
        group_data = utils.group_by_weekday(sample_data[10])
        self.assertEqual(
            group_data, [[], [30047], [24465], [23705], [], [], []]
        )
        group_data = utils.group_by_weekday(sample_data[11])
        self.assertEqual(
            group_data,
            [[24123], [16564], [25321], [22969, 22999], [6426], [], []]
>>>>>>> 8e9f1a211f3eae65f2eabbb8136192add006c466
        )

    def test_seconds_since_midnight(self):
        mid_data = utils.seconds_since_midnight(datetime.time(17, 0, 42))
<<<<<<< HEAD
        self.assertIsInstance(mid_data, int)
        self.assertIn(mid_data, [y for y in range(60500, 61500)])
        self.assertIsNotNone(mid_data)
        self.assertLess(mid_data, 70000)
        assert mid_data != 0

    def test_interval(self):
        inter_data = utils.interval(datetime.time(16, 0, 40),
                                    datetime.time(17, 0, 42))
        self.assertIsInstance(inter_data, int)
        self.assertIn(inter_data, [z for z in range(3500, 4500)])
        self.assertLess(inter_data, 5000)
        self.assertIsNotNone(inter_data)
        self.assertNotAlmostEqual(inter_data, 1)

    def test_mean(self):
        mean_data = utils.mean([37435, 67])
        self.assertIsInstance(mean_data, float)
        self.assertLess(mean_data, 50000)
        self.assertNotAlmostEqual(mean_data, 3)
        self.assertIsNotNone(mean_data)
=======
        self.assertEqual(mid_data, 61242)
        mid_data = utils.seconds_since_midnight(datetime.time(16, 7, 41))
        self.assertEqual(mid_data, 58061)
        mid_data = utils.seconds_since_midnight(datetime.time(12, 47, 46))
        self.assertEqual(mid_data, 46066)

    def test_interval(self):
        inter_data = utils.interval(
            datetime.time(16, 0, 40),
            datetime.time(17, 0, 42)
        )
        self.assertEqual(inter_data, 3602)
        inter_data = utils.interval(
            datetime.time(8, 19, 37),
            datetime.time(17, 0, 42)
        )
        self.assertEqual(inter_data, 31265)
        inter_data = utils.interval(
            datetime.time(11, 2, 21),
            datetime.time(16, 50, 17)
        )
        self.assertEqual(inter_data, 20876)
        inter_data = utils.interval(
            datetime.time(7, 51, 28),
            datetime.time(16, 38, 58)
        )
        self.assertEqual(inter_data, 31650)

    def test_mean(self):
        mean_data = utils.mean([
            31938,
            106,
            29817,
            29992,
        ])
        self.assertEqual(mean_data, 22963.25)
        mean_data = utils.mean([
            36271,
            34577,
            30658,
            29401,
            29655,
        ])
        self.assertEqual(mean_data, 32112.4)
        mean_data = utils.mean([
            26136,
            27895,
            31253,
            31759,
            41026,
        ])
        self.assertEqual(mean_data, 31613.8)
        mean_data = utils.mean([])
        self.assertEqual(mean_data, 0)
>>>>>>> 8e9f1a211f3eae65f2eabbb8136192add006c466


def suite():
    """
    Default test suite.
    """
    base_suite = unittest.TestSuite()
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerViewsTestCase))
    base_suite.addTest(unittest.makeSuite(PresenceAnalyzerUtilsTestCase))
    return base_suite


if __name__ == '__main__':
    unittest.main()
