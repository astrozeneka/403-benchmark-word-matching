#!/usr/bin/env python3
"""Trie-based baseline: per-article character trie (ported from src/main.cpp
via Cython, see src/trie.hpp / src/trie.pyx) instead of one regex per keyword.
Run against the same cached dataset as 001_naive.py so timings are comparable.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from _dataset import load_dataset, load_keywords
import trie_matcher


def compute_scores(articles, keywords):
    scores = []
    for article in articles:
        text = article["text"]
        word_count = len(text.split())

        trie = trie_matcher.PyWordTrie()
        trie.build(text)
        total_score = sum(trie.score(keyword) for keyword in keywords)

        normalized_score = total_score / word_count if word_count else 0
        scores.append((article["id"], normalized_score))
    return scores


if __name__ == "__main__":
    keywords = load_keywords()
    articles = load_dataset()

    start = time.perf_counter()
    scores = compute_scores(articles, keywords)
    elapsed = time.perf_counter() - start

    print(f"articles={len(articles)} keywords={len(keywords)}")
    print(f"elapsed={elapsed:.4f}s avg_per_article={elapsed / len(articles):.6f}s")
