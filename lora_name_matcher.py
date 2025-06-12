"""
Enhanced LoRA name matching utilities for better CivitAI search results
"""

import re
import requests
from typing import List, Tuple, Optional


class LoRANameMatcher:
    """Smart LoRA name matching for CivitAI search"""

    def __init__(self):
        self.skip_words = {'lora', 'model', 'sd',
                           'xl', 'v1', 'v2', 'the', 'and', 'or', 'of'}

    def normalize_name_for_search(self, name: str) -> str:
        """Normalize a LoRA name for better matching"""
        # Remove file extensions
        name = re.sub(r'\.(safetensors|ckpt|pt)$',
                      '', name, flags=re.IGNORECASE)

        # Convert to lowercase first for consistent processing
        name = name.lower()

        # Handle common abbreviations and fix concatenated words
        # Replace common patterns where words are stuck together
        name = re.sub(r'breastin', 'breast in', name)
        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)  # camelCase
        # letter followed by number
        name = re.sub(r'([a-z])(\d)', r'\1 \2', name)
        # number followed by letter
        name = re.sub(r'(\d)([a-z])', r'\1 \2', name)

        # Convert separators to spaces
        name = re.sub(r'[_-]+', ' ', name)  # underscores and dashes

        # Remove version patterns
        name = re.sub(r'\bv\d+(\.\d+)?\b', '', name,
                      flags=re.IGNORECASE)  # v1, v16, v1.5
        name = re.sub(r'\b(sd|xl)\d*(\.\d+)?\b', '', name,
                      flags=re.IGNORECASE)  # SD1.5, XL

        # Clean up extra spaces and common suffixes
        name = re.sub(r'\b(lora|model)s?\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+', ' ', name).strip()

        return name

    def extract_search_keywords(self, lora_name: str) -> List[str]:
        """Extract meaningful keywords from LoRA filename for search"""
        normalized = self.normalize_name_for_search(lora_name)

        # Split into potential keywords
        words = normalized.split()

        # Filter out very short words and common terms
        keywords = []
        for word in words:
            if len(word) >= 3 and word.lower() not in self.skip_words:
                keywords.append(word)

        return keywords

    def calculate_name_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity between two names using multiple methods"""
        def levenshtein_distance(s1: str, s2: str) -> int:
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)
            if len(s2) == 0:
                return len(s1)

            previous_row = list(range(len(s2) + 1))
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(
                        min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        # Normalize both names
        norm1 = self.normalize_name_for_search(name1).lower()
        norm2 = self.normalize_name_for_search(name2).lower()

        # Calculate different similarity metrics

        # 1. Exact match after normalization
        if norm1 == norm2:
            return 1.0

        # 2. One contains the other
        if norm1 in norm2 or norm2 in norm1:
            return 0.8

        # 3. Levenshtein distance similarity
        max_len = max(len(norm1), len(norm2))
        if max_len == 0:
            return 0.0
        distance = levenshtein_distance(norm1, norm2)
        lev_similarity = 1.0 - (distance / max_len)

        # 4. Word overlap similarity
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        if len(words1) == 0 and len(words2) == 0:
            return 1.0
        if len(words1) == 0 or len(words2) == 0:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        word_similarity = intersection / union if union > 0 else 0.0

        # Combine similarities with weights
        combined_similarity = (lev_similarity * 0.4) + (word_similarity * 0.6)

        return max(combined_similarity, 0.0)

    def find_best_match_from_search_results(self, lora_name: str, search_results: List[dict]) -> Tuple[Optional[dict], float]:
        """Find the best matching LoRA from search results"""
        if not search_results:
            return None, 0.0

        best_match = None
        best_similarity = 0.0

        # Remove duplicates
        seen_ids = set()
        unique_results = []
        for item in search_results:
            item_id = item.get("id")
            if item_id not in seen_ids:
                seen_ids.add(item_id)
                unique_results.append(item)

        # Find best match using similarity scoring
        for item in unique_results:
            item_name = item.get("name", "")

            # Check against model name
            similarity = self.calculate_name_similarity(lora_name, item_name)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = item

            # Also check model versions for filename matches
            model_versions = item.get("modelVersions", [])
            for version in model_versions:
                files = version.get("files", [])
                for file_info in files:
                    file_name = file_info.get("name", "")
                    similarity = self.calculate_name_similarity(
                        lora_name, file_name)
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = item

        return best_match, best_similarity

    def search_civitai_with_multiple_strategies(self, lora_name: str, civitai_token: str) -> Tuple[List[dict], List[str]]:
        """Search CivitAI using multiple strategies and return all results"""
        headers = {"Authorization": f"Bearer {civitai_token}"}
        search_url = "https://civitai.com/api/v1/models"

        # Try multiple search strategies
        search_strategies = []

        # Strategy 1: Use original name
        search_strategies.append(("original", lora_name))

        # Strategy 2: Use normalized name
        normalized = self.normalize_name_for_search(lora_name)
        if normalized != lora_name and normalized.strip():
            search_strategies.append(("normalized", normalized))

        # Strategy 3: Use keywords
        keywords = self.extract_search_keywords(lora_name)
        if keywords:
            # Try with top 3 keywords
            keyword_query = " ".join(keywords[:3])
            search_strategies.append(("keywords", keyword_query))

            # Try with just the first keyword if it's long enough
            if len(keywords[0]) >= 5:
                search_strategies.append(("first_keyword", keywords[0]))

        all_results = []
        used_queries = []

        # Try each search strategy
        for strategy_name, search_query in search_strategies:
            if not search_query.strip():
                continue

            params = {
                "query": search_query,
                "types": "LORA",
                "sort": "Highest Rated",
                "limit": 10  # Get more results for better matching
            }

            try:
                response = requests.get(
                    search_url, headers=headers, params=params, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    items = data.get("items", [])
                    all_results.extend(items)
                    used_queries.append(
                        f"{strategy_name}: '{search_query}' ({len(items)} results)")
                else:
                    used_queries.append(
                        f"{strategy_name}: '{search_query}' (HTTP {response.status_code})")
            except Exception as e:
                used_queries.append(
                    f"{strategy_name}: '{search_query}' (Error: {str(e)})")

        return all_results, used_queries


# Example usage for testing:
if __name__ == "__main__":
    matcher = LoRANameMatcher()

    # Test normalization
    test_names = []

    print("Name Normalization Tests:")
    for name in test_names:
        normalized = matcher.normalize_name_for_search(name)
        keywords = matcher.extract_search_keywords(name)
        print(f"Original: {name}")
        print(f"Normalized: {normalized}")
        print(f"Keywords: {keywords}")
        print("-" * 40)
