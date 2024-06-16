import os
import unittest

from server.worker.process_csv_file_chunk import get_chunk


TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), "data/data_1.csv")


class GetChunkTest(unittest.TestCase):
    def test_get_chunk_0(self):
        chunk = get_chunk(file_path=TESTDATA_FILENAME, chunk_index=0, chunksize=2)
        expected = [
            {
                "sensorName": "Gyroscope 1",
                "timestamp": "invalid timestamp",
                "value": 512.1067925517784,
            },
            {
                "sensorName": "Temperature Sensor 1",
                "timestamp": "1991-05-17T01:41:02.624873+08:00",
                "value": 942.666003964492,
            },
        ]
        self.assertEqual(chunk.to_dict("records"), expected)

    def test_get_chunk_5(self):
        chunk = get_chunk(file_path=TESTDATA_FILENAME, chunk_index=4, chunksize=2)
        expected = [
            {
                "sensorName": "Humidity Sensor 1",
                "timestamp": "1996-06-29T03:32:51.625388+08:00",
                "value": 828.31492649431,
            }
        ]
        self.assertEqual(chunk.to_dict("records"), expected)
