#!/usr/bin/env python3
"""
测试SDSS数据获取的简化版本
"""

import requests
import pandas as pd
from io import StringIO
import time

def test_sdss_with_different_sizes():
    """测试不同数据量下的SDSS查询性能"""
    
    url = "https://skyserver.sdss.org/dr16/en/tools/search/x_sql.aspx"
    
    # 测试不同的数据量
    test_sizes = [5, 10, 25, 50, 100]
    
    for size in test_sizes:
        print(f"\n=== Testing {size} galaxies ===")
        
        query = f"""
        SELECT TOP {size}
            objid, ra, dec, petroMag_r, 
            petroR50_r, deVAB_r
        FROM PhotoObj 
        WHERE type = 3 
            AND petroMag_r BETWEEN 15 AND 18
            AND petroR50_r > 0
        """
        
        start_time = time.time()
        try:
            response = requests.get(
                url, 
                params={'cmd': query, 'format': 'csv'}, 
                timeout=20
            )
            end_time = time.time()
            
            if response.status_code == 200:
                # Parse data
                lines = response.text.strip().split('\n')
                if lines[0].startswith('#'):
                    csv_content = '\n'.join(lines[1:])
                else:
                    csv_content = response.text
                
                df = pd.read_csv(StringIO(csv_content))
                
                print(f"✓ SUCCESS: {len(df)} galaxies in {end_time - start_time:.2f}s")
                print(f"  Columns: {list(df.columns)}")
                print(f"  Sample: objid={df.iloc[0]['objid']}, ra={df.iloc[0]['ra']:.3f}")
                
                if size >= 50:
                    print("  This size works! Can use real SDSS data.")
                    return True
                    
            else:
                print(f"✗ HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            end_time = time.time()
            print(f"✗ TIMEOUT after {end_time - start_time:.2f}s")
        except Exception as e:
            end_time = time.time()
            print(f"✗ ERROR: {e}")
    
    return False

if __name__ == "__main__":
    print("SDSS Connection Test")
    print("=" * 40)
    
    success = test_sdss_with_different_sizes()
    
    if success:
        print("\n🎉 SDSS connection is working!")
        print("The galaxy_morphology_art.py program should be able to fetch real data.")
    else:
        print("\n⚠️  SDSS connection has issues")
        print("The program will use synthetic data instead.")