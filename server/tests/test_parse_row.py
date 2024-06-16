import unittest
from datetime import datetime
from dateutil import tz

from server.worker.process_csv_file_chunk import parse_row


class ParseRowTest(unittest.TestCase):
    def test_parse_row_success(self):
        data = {
            "sensorName": "test_sensor",
            "timestamp": "1991-05-17T01:41:02.624873+08:00",
            "value": "947.1455281490692",
        }
        parsed_row = parse_row(data, "test.csv")

        tzinfo = tz.gettz("Asia/Hong_Kong")
        expected = {
            "sensor_name": "test_sensor",
            "timestamp": datetime(1991, 5, 17, 1, 41, 2, 624873, tzinfo),
            "value": 947.1455281490692,
        }

        self.assertEqual(parsed_row, expected)

    def test_parse_row_failed(self):
        data = {
            "sensorName": "test_sensor",
            "timestamp": "invalid_dateformat",
            "value": "947.1455281490692",
        }
        parsed_row = parse_row(data, "test.csv")

        self.assertIsNone(parsed_row)
