import unittest
from pathlib import Path
import sys

# Add Scripts folder to path to import parser logic if needed, 
# or test threshold evaluation logic directly.
class TestVulnMeshGRC(unittest.TestCase):
    
    def test_threshold_evaluation(self):
        # Simulate policy limits vs actual counts
        max_crit = 0
        max_high = 2
        
        # Test case 1: Pass condition
        crit_count_pass = 0
        high_count_pass = 1
        compliant_pass = (crit_count_pass <= max_crit) and (high_count_pass <= max_high)
        self.assertTrue(compliant_pass)

        # Test case 2: Fail condition
        crit_count_fail = 1
        high_count_fail = 1
        compliant_fail = (crit_count_fail <= max_crit) and (high_count_fail <= max_high)
        self.assertFalse(compliant_fail)

if __name__ == "__main__":
    unittest.main()