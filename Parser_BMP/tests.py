import unittest

from parser_bitmap import ParserBMP


class Test(unittest.TestCase):
    def setUp(self):
        self.p = ParserBMP(r'pictures/aloe.bmp')

    def test_bmp_filename(self):
        result = self.p.get_filename()
        self.assertEqual('aloe', result['Filename'])

    def test_no_bmp_file(self):
        p_2 = ParserBMP(r'pictures/noBMP.jpg')
        self.assertRaises(UnicodeDecodeError, p_2.get_file_header_data())

    def test_bmp_data_header(self):
        result = self.p.get_file_header_data()
        self.assertEqual('BM', result['Signature'])
        self.assertEqual(262282, result['File size'])
        self.assertEqual(0, result['Reserved bytes'])
        self.assertEqual(138, result['Offset'])

    def test_version_bmp(self):
        ""
        """
        fileCORE = self.p.get_bitmap_header_data(...)
        self.assertEqual(12, fileCORE['Header length'])
        self.assertEqual('CORE', fileCORE['File version'])
        """
        p_2 = ParserBMP(r'pictures/debugging.bmp')
        fileV3 = p_2.get_bitmap_header_data()
        self.assertEqual(40, fileV3['Header length'])
        self.assertEqual('Windows V3', fileV3['File version'])

        """
        fileV4 = self.p.get_bitmap_header_data(...)
        self.assertEqual(108, fileV4['Header length'])
        self.assertEqual('Windows V4', fileV4['File version'])
        """

        fileV5 = self.p.get_bitmap_header_data()
        self.assertEqual(124, fileV5['Header length'])
        self.assertEqual('Windows V5', fileV5['File version'])

    def test_data_header_bmp_V3(self):
        result = self.p.get_bitmap_header_data()
        self.assertEqual(256, result['Width'])
        self.assertEqual(256, result['Height'])
        self.assertEqual(1, result['Planes'])
        self.assertEqual(32, result['Count bits'])
        self.assertEqual(3, result['Compression'])
        self.assertEqual(262144, result['Size image'])
        self.assertEqual(2835, result['Horizontal pixels per meter'])
        self.assertEqual(2835, result['Vertical pixels per meter'])
        self.assertEqual(0, result['Count colors'])
        self.assertEqual(0, result['Count important colors'])

    def test_data_header_bmp_V5(self):
        result = self.p.get_bitmap_header_data()
        self.assertEqual(16711680, result['Red mask'])
        self.assertEqual(65280, result['Green mask'])
        self.assertEqual(255, result['Blue mask'])
        self.assertEqual(4278190080, result['Alpha mask'])
        self.assertEqual('sRGB', result['Color space type'])

        self.assertEqual(4, result['Intent'])
        self.assertEqual(0, result['Profile data'])
        self.assertEqual(0, result['Profile size'])
        self.assertEqual(0, result['Reserved'])

