import sys
import os
sys.path.append(os.path.dirname(__file__))

from lora_name_matcher import LoRANameMatcher

# Test the enhanced matching
matcher = LoRANameMatcher()

test_names = [
    "example_lora_v1.safetensors",
    "test_model_v2.1.ckpt", 
    "sample_lora_v3.safetensors"
]

print("Enhanced LoRA Name Matching Test:")
print("=" * 50)

for name in test_names:
    print(f"\nOriginal: {name}")
    normalized = matcher.normalize_name_for_search(name)
    print(f"Normalized: {normalized}")
    keywords = matcher.extract_search_keywords(name)
    print(f"Keywords: {keywords}")
    print("-" * 30)

print("\nSimilarity test:")
similarity = matcher.calculate_name_similarity(
    "example_lora_v1", 
    "Example LoRA Model"
)
print(f"Similarity between 'example_lora_v1' and 'Example LoRA Model': {similarity:.2f}")
