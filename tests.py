import unittest

from utils import checkLatitude, checkLongitude, fileType, addressResolver
from etl import extract, etlProcess
from exceptions import LatitudeWrongValue, LongitudeWrongValue, NotAType, NoInputFiles

class TestUtils(unittest.TestCase):
    def test_checkLatitude(self):
        self.assertEqual(checkLatitude(-90), True)
        self.assertEqual(checkLatitude(90), True)
        self.assertEqual(checkLatitude(-90.0), True)
        self.assertEqual(checkLatitude(90.0), True)
        with self.assertRaises(LatitudeWrongValue): checkLatitude(-91)
        with self.assertRaises(LatitudeWrongValue): checkLatitude(91)
        with self.assertRaises(LatitudeWrongValue): checkLatitude(-90.001)
        with self.assertRaises(LatitudeWrongValue): checkLatitude(90.001)

    def test_checkLongitude(self):
        self.assertEqual(checkLongitude(-180), True)
        self.assertEqual(checkLongitude(180), True)
        self.assertEqual(checkLongitude(-180.0), True)
        self.assertEqual(checkLongitude(180.0), True)
        with self.assertRaises(LongitudeWrongValue): checkLongitude(-181)
        with self.assertRaises(LongitudeWrongValue): checkLongitude(181)
        with self.assertRaises(LongitudeWrongValue): checkLongitude(-180.001)
        with self.assertRaises(LongitudeWrongValue): checkLongitude(180.001)

    def test_fileType(self):
        self.assertEqual(fileType('teste.txt'), '.txt')
        self.assertEqual(fileType('teste.tar.gz'), '.tar.gz')
        self.assertEqual(fileType('teste'), '')

    def test_addressResolver(self):
        with self.assertRaises(KeyError): addressResolver({}, None)
        with self.assertRaises(TypeError): addressResolver({'address_components': ''}, None)

class TestETL(unittest.TestCase):
    def test_etlProcess(self):
        with self.assertRaises(TypeError): etlProcess(None)
        with self.assertRaises(NoInputFiles): etlProcess('')
        self.assertEqual(etlProcess(['data_points.tar.gz']), True)

    def test_extract(self):
        with self.assertRaises(FileNotFoundError): extract('teste.teste')
        with self.assertRaises(NotAType): extract('etl.py')


if __name__ == "__main__":
    unittest.main()
