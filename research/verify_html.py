import json
import os
import re

def verify_html_structure():
    html_path = "/Users/aadityamohansamadhiya/Composio/composio-agent-research/reports/index.html"
    if not os.path.exists(html_path):
        print(f"[Error] index.html not found at {html_path}")
        return False
        
    with open(html_path, "r") as f:
        html = f.read()
        
    checks = {
        "HTML Document tag": "</html>" in html,
        "Tailwind CDN script": "cdn.tailwindcss.com" in html,
        "ChartJS CDN script": "cdn.jsdelivr.net/npm/chart.js" in html,
        "Auth Chart canvas": 'id="authChart"' in html,
        "Verdict Chart canvas": 'id="verdictChart"' in html,
        "Blockers Chart canvas": 'id="blockersChart"' in html,
        "Category Chart canvas": 'id="categoryChart"' in html,
        "Search input box": 'id="tableSearch"' in html,
        "Category filter dropdown": 'id="filterCategory"' in html,
        "Table element": "<table" in html,
        "Table body placeholder": 'id="tableBody"' in html,
        "Pagination controls": 'id="prevBtn"' in html and 'id="nextBtn"' in html
    }
    
    print("="*60)
    print("           PROGRAMMATIC HTML INTEGRITY CHECK          ")
    print("="*60)
    
    failed = 0
    for name, success in checks.items():
        status = "[✓] PASS" if success else "[✗] FAIL"
        if not success:
            failed += 1
        print(f"{name:<35}: {status}")
        
    # Extract and parse inlined dataset JSON
    dataset_match = re.search(r"const dataset = (\[.*?\]);", html, re.DOTALL)
    if dataset_match:
        try:
            dataset_json = json.loads(dataset_match.group(1))
            print(f"{'Inlined Dataset Parse':<35}: [✓] PASS (Parsed {len(dataset_json)} apps)")
            if len(dataset_json) != 100:
                print(f"[Error] Expected 100 records, got {len(dataset_json)}")
                failed += 1
        except Exception as e:
            print(f"{'Inlined Dataset Parse':<35}: [✗] FAIL ({e})")
            failed += 1
    else:
        print(f"{'Inlined Dataset Match':<35}: [✗] FAIL")
        failed += 1

    # Extract and parse inlined patterns JSON
    patterns_match = re.search(r"const patterns = (\{.*?\});", html, re.DOTALL)
    if patterns_match:
        try:
            patterns_json = json.loads(patterns_match.group(1))
            print(f"{'Inlined Patterns Parse':<35}: [✓] PASS")
        except Exception as e:
            print(f"{'Inlined Patterns Parse':<35}: [✗] FAIL ({e})")
            failed += 1
    else:
        print(f"{'Inlined Patterns Match':<35}: [✗] FAIL")
        failed += 1
        
    print("="*60)
    if failed == 0:
        print("RESULT: ALL INTEGRITY CHECKS PASSED!")
        return True
    else:
        print(f"RESULT: {failed} CHECKS FAILED.")
        return False

if __name__ == "__main__":
    verify_html_structure()
