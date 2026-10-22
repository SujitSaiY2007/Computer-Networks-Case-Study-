import unittest
from python.features import aggregate,FEATURE_NAMES

class FeatureTests(unittest.TestCase):
    def test_deterministic_aggregation(self):
        events=[{"t0_ns":100,"event_type":1,"pid":10},{"t0_ns":200,"event_type":3,"pid":10},{"t0_ns":1_000_000_100,"event_type":2,"pid":11}]
        a=aggregate(events)
        b=aggregate(events)
        self.assertEqual(a,b)
        self.assertEqual(a[0]["exec_count"],1.0)
        self.assertEqual(a[0]["connect_count"],1.0)
        self.assertEqual(a[0]["unique_process_count"],1.0)
        self.assertEqual(len(FEATURE_NAMES),5)

if __name__=="__main__": unittest.main()
