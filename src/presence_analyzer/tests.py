# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
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
        self.assertDictEqual(data[0], {u'user_id': 10, u'name': u'User 10'})

    def test_mean_time_weekday_view(self):
        mean_time_data = views.mean_time_weekday_view(10)
        self.assertEqual(mean_time_data.content_type, 'application/json')
        data = json.loads(mean_time_data.data)
        self.assertNotEqual(len(data), 0)
        self.assertNotEqual(mean_time_data.status_code, 404)
        self.assertEqual(mean_time_data.status_code, 200)

    def test_presence_weekday_view(self):
        # import ipdb; ipdb.set_trace()
        presence_data = views.presence_weekday_view(10)
        self.assertEqual(presence_data.content_type, 'application/json')
        data = json.loads(presence_data.data)
        self.assertNotEqual(len(data), 0)
        self.assertNotEqual(presence_data.status_code, 404)
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
        )

    def test_seconds_since_midnight(self):
        mid_data = utils.seconds_since_midnight(datetime.time(17, 0, 42))
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
