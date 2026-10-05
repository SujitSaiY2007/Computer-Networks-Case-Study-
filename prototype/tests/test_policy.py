import unittest
from python.policy import Policy,Stage

class PolicyTests(unittest.TestCase):
    def test_safe_default(self):
        p=Policy(0.5,allow_mitigation=False)
        self.assertEqual(p.evaluate(0.9,"x"),Stage.DETECT_LOG)
        self.assertFalse(p.request_mitigation("x"))
        p.rollback("x")
        self.assertEqual(p.stage,Stage.OBSERVE)

if __name__=="__main__": unittest.main()
