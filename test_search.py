#!/usr/bin/env python3
"""
Test script to verify Technical Design search functionality works correctly.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_search():
    print("Starting Technical Design search test...")
    
    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Chrome WebDriver not available: {e}")
        print("Please test manually by:")
        print("1. Opening http://127.0.0.1:8080/ in browser")
        print("2. Clicking 'Technical Design' tab")
        print("3. Entering search terms in the search field")
        print("4. Verifying no console errors and results appear")
        return
    
    try:
        # Navigate to the web UI
        driver.get("http://127.0.0.1:8080/")
        
        # Wait for page load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "tech-design-tab")))
        
        # Click Technical Design tab
        tech_design_tab = driver.find_element(By.ID, "tech-design-tab")
        tech_design_tab.click()
        
        # Wait for search input to appear
        time.sleep(1)
        search_input = wait.until(EC.presence_of_element_located((By.ID, "tech-design-search")))
        
        # Test 1: Search for "product"
        print("\nTest 1: Searching for 'product'...")
        search_input.clear()
        search_input.send_keys("product")
        time.sleep(1)
        
        # Check for JavaScript errors in console
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        
        if errors:
            print("❌ FAILED: JavaScript errors found:")
            for error in errors:
                print(f"  {error['message']}")
            return False
        else:
            print("✓ No JavaScript errors")
        
        # Check if results are displayed
        accordion = driver.find_element(By.ID, "tech-design-accordion")
        if accordion.text.strip():
            print("✓ Search results displayed")
        else:
            print("⚠ Warning: No results displayed (might be expected if no matches)")
        
        # Test 2: Clear search
        print("\nTest 2: Clearing search...")
        search_input.clear()
        time.sleep(1)
        
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        
        if errors:
            print("❌ FAILED: JavaScript errors found when clearing search:")
            for error in errors:
                print(f"  {error['message']}")
            return False
        else:
            print("✓ No errors when clearing search")
        
        # Test 3: Search with no results
        print("\nTest 3: Searching for 'xyz123' (should have no results)...")
        search_input.clear()
        search_input.send_keys("xyz123")
        time.sleep(1)
        
        logs = driver.get_log('browser')
        errors = [log for log in logs if log['level'] == 'SEVERE']
        
        if errors:
            print("❌ FAILED: JavaScript errors found:")
            for error in errors:
                print(f"  {error['message']}")
            return False
        else:
            print("✓ No errors with no-results search")
        
        # Check for "no results" message
        accordion = driver.find_element(By.ID, "tech-design-accordion")
        if "no matching questions" in accordion.text.lower():
            print("✓ 'No results' message displayed correctly")
        
        print("\n✅ All tests passed! Search functionality works correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    success = test_search()
    sys.exit(0 if success else 1)
