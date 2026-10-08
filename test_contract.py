import copy
import unittest
from geojson_delivery_contract import check

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.data = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"id":"a","name":"Station"},"geometry":{"type":"Point","coordinates":[54,24]}}]}
        self.contract = {"geometry_types":["Point"],"required_properties":["name"],"id_property":"id","bounds":[50,20,60,30]}
    def test_good(self):
        self.assertTrue(check(self.data,self.contract)["ok"])
    def test_duplicate(self):
        self.data["features"] *= 2
        self.assertEqual(check(self.data,self.contract)["findings"][0]["code"],"duplicate_id")
    def test_missing(self):
        del self.data["features"][0]["properties"]["name"]
        self.assertFalse(check(self.data,self.contract)["ok"])
    def test_outside(self):
        self.data["features"][0]["geometry"]["coordinates"]=[64,24]
        self.assertEqual(check(self.data,self.contract)["findings"][0]["code"],"outside_delivery_bounds")
    def test_dateline(self):
        self.contract["bounds"]=[170,-20,-170,30]
        self.data["features"][0]["geometry"]["coordinates"]=[-175,24]
        self.assertTrue(check(self.data,self.contract)["ok"])
    def test_bool_coordinate(self):
        self.data["features"][0]["geometry"]["coordinates"]=[True,24]
        with self.assertRaises(ValueError):check(self.data,self.contract)
    def test_nonfinite(self):
        self.data["features"][0]["geometry"]["coordinates"]=[float("nan"),24]
        with self.assertRaises(ValueError):check(self.data,self.contract)
    def test_no_mutation(self):
        before=copy.deepcopy(self.data);check(self.data,self.contract);self.assertEqual(before,self.data)
    def test_unknown_contract(self):
        with self.assertRaises(ValueError):check(self.data,{"mni_features":1})
    def test_nested_polygon(self):
        self.data["features"][0]["geometry"]={"type":"Polygon","coordinates":[[[54,24],[55,24],[55,25],[54,24]]]}
        self.contract["geometry_types"]=["Polygon"]
        self.assertEqual(check(self.data,self.contract)["positions"],4)

if __name__=="__main__":unittest.main()
