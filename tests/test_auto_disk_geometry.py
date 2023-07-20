from unittest import TestCase
from amitoolhelpers.disk_geometry import AutoDiskGeometry

class TestAutoDiskGeometery(TestCase):

    def test_mb_values(self):
        for i in range(1,1024*1024):
            adg = AutoDiskGeometry(i)
            self.assertIsNotNone(adg.size, msg='Failed Value: {}'.format(i))
