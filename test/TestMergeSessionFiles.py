import unittest

from MergeSessionFiles import SessionLoader


class TestSessionLoader(unittest.TestCase):
    '''
    Test session loader methods
    '''

    def __init__(self):
        self.sessionLoader = SessionLoader()
        
    def test_consolidate(self):
        file_path = "C://Users//Chris//Documents//GitHub//DW_Microtasks//test//testData.txt"
        file_lines = self.sessionLoader.load_file(file_path)
        file_lines = self.sessionLoader.consolidate_broken_explanations(file_lines)
        file_lines
        self.assertEqual(3,file_lines.__len__())

unittest.main()
