#!/usr/bin/env python3
"""Naive (regex-per-keyword) baseline, reproducing the scoring logic of
403-proj001-peaks-and-valleys/002_compute_score.py, run against a fixed,
locally cached dataset so timings are comparable across runs/implementations.
"""
import re
import time

from _dataset import load_dataset, load_keywords


def compute_scores(articles, keywords):
    scores = []
    for article in articles:
        text = article["text"]
        word_count = len(text.split())
        total_score = 0
        for keyword in keywords:
            count = len(re.findall(r"\b" + re.escape(keyword) + r"\b", text, flags=re.IGNORECASE))
            total_score += count
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
