import sys
import os
sys.path.append(os.path.dirname(__file__))

from lora_name_matcher import LoRANameMatcher
import requests

def test_civitai_search(lora_name, token=""):
    """Test actual CivitAI search for a LoRA"""
    print(f"\n🔍 Testing CivitAI search for: {lora_name}")
    print("=" * 50)
    
    # Test the search strategies
    matcher = LoRANameMatcher()
    
    # Show what search terms will be used
    print("Search strategies:")
    print(f"1. Original: '{lora_name}'")
    
    normalized = matcher.normalize_name_for_search(lora_name)
    print(f"2. Normalized: '{normalized}'")
    
    keywords = matcher.extract_search_keywords(lora_name)
    if keywords:
        keyword_query = " ".join(keywords[:3])
        print(f"3. Keywords: '{keyword_query}'")
    
    # Try actual API call (without token)
    search_url = "https://civitai.com/api/v1/models"
    
    for i, query in enumerate([lora_name, normalized, keyword_query if keywords else ""], 1):
        if not query.strip():
            continue
            
        print(f"\nTrying search {i}: '{query}'")
        
        params = {
            "query": query,
            "types": "LORA",
            "sort": "Highest Rated",
            "limit": 5
        }
        
        try:
            response = requests.get(search_url, params=params, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                print(f"Results: {len(items)} models found")
                for j, item in enumerate(items[:3], 1):
                    name = item.get("name", "Unknown")
                    similarity = matcher.calculate_name_similarity(lora_name, name)
                    model_id = item.get("id", "N/A")
                    
                    # Check if model has downloadable versions
                    versions = item.get("modelVersions", [])
                    has_files = False
                    if versions:
                        files = versions[0].get("files", [])
                        has_files = len(files) > 0
                        if files:
                            primary_file = files[0]
                            download_url = primary_file.get("downloadUrl")
                            requires_auth = "Authorization required" if not download_url else "Public download"
                    
                    print(f"  {j}. {name} (similarity: {similarity:.2f})")
                    print(f"     ID: {model_id}, Files: {len(files) if versions else 0}, Auth: {requires_auth if has_files else 'No files'}")
            else:
                print(f"Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")

# Test example LoRAs
test_loras = ["example_lora", "test_model"]

for lora in test_loras:
    test_civitai_search(lora)
