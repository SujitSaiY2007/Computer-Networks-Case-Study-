import unittest
from python.model import train,score
from python.features import FEATURE_NAMES

class ModelTests(unittest.TestCase):
    def test_schema_rejection_and_determinism(self):
        rows=[]
        for i in range(6):
            rows.append({n:float(i+(j%2)) for j,n in enumerate(FEATURE_NAMES)})
        labels=[0,1,0,1,0,1]
        artifact=train(rows,labels)
        self.assertEqual(score(artifact,rows[0]),score(artifact,rows[0]))
        artifact["feature_names"]=artifact["feature_names"][:-1]
        with self.assertRaises(ValueError): score(artifact,rows[0])

if __name__=="__main__": unittest.main()
