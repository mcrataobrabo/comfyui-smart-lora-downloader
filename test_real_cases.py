import sys
import os
sys.path.append(os.path.dirname(__file__))

from lora_name_matcher import LoRANameMatcher

# Test with example cases
matcher = LoRANameMatcher()

test_cases = [
    {
        "comfyui_name": "example_model_v1",
        "civitai_name": "Example Model LoRA - SD1.5"
    },
    {
        "comfyui_name": "test_lora", 
        "civitai_name": "TestLoRA-StyleTransfer"
    }
]

print("Testing LoRA Name Matching:")
print("=" * 50)

for i, case in enumerate(test_cases, 1):
    comfy_name = case["comfyui_name"]
    civit_name = case["civitai_name"]
    
    print(f"\nTest Case {i}:")
    print(f"ComfyUI name: {comfy_name}")
    print(f"CivitAI name:  {civit_name}")
    
    # Test normalization
    norm_comfy = matcher.normalize_name_for_search(comfy_name)
    norm_civit = matcher.normalize_name_for_search(civit_name)
    
    print(f"Normalized ComfyUI: {norm_comfy}")
    print(f"Normalized CivitAI:  {norm_civit}")
    
    # Test keywords
    keywords_comfy = matcher.extract_search_keywords(comfy_name)
    keywords_civit = matcher.extract_search_keywords(civit_name)
    
    print(f"Keywords ComfyUI: {keywords_comfy}")
    print(f"Keywords CivitAI:  {keywords_civit}")
    
    # Test similarity
    similarity = matcher.calculate_name_similarity(comfy_name, civit_name)
    print(f"Similarity Score: {similarity:.2f}")
    
    # Test if this would pass the threshold
    threshold = 0.3
    would_match = similarity >= threshold
    print(f"Would match (>= {threshold}): {'✅ YES' if would_match else '❌ NO'}")
    
    print("-" * 50)
