# 403-benchmark-word-matching

Benchmarks for keyword-matching strategies used to score articles against a
stock's keyword list (same scoring logic as
`403-proj001-peaks-and-valleys/002_compute_score.py`: total keyword hits in
an article's text, normalized by word count).

Two implementations, timed against the same cached dataset:

- `benchmark/001_naive.py` — one case-insensitive regex (`\bkeyword\b`) per
  keyword, run over the raw text. This is what production currently does.
- `benchmark/002_trie.py` — builds a per-article character trie (ported from
  `src/main.cpp` via Cython) and looks up each keyword's occurrence count in
  the trie instead of running a regex.

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install psycopg2-binary cython setuptools
./.venv/bin/python setup.py build_ext --inplace   # compiles src/trie.pyx -> trie_matcher*.so
```

A local Postgres with the `articles` table must be reachable (defaults to
`postgresql://postgres:postgres@localhost:5432/postgres`, override with the
`DATABASE_URL` env var).

## Running a benchmark

```bash
./.venv/bin/python benchmark/001_naive.py
./.venv/bin/python benchmark/002_trie.py
```

On first run, each script downloads `DATASET_SIZE` articles (currently
2^12 = 4096, see `benchmark/_dataset.py`) and caches them to
`benchmark/data/tsla_articles.json` so every subsequent run — and every
implementation — is timed against the exact same input. Delete that file to
re-download. Keywords are read from `benchmark/keywords_tsla.txt` (TSLA
keyword list).

Each script prints total elapsed time and average time per article.

## Trie implementation notes

`src/trie.hpp` is a reusable C++ port of the `Node`/`buildTree`/
`_compute_word_score` logic in `src/main.cpp` (the original CLI tool is left
untouched). `src/trie.pyx` wraps it as a Cython extension class
(`PyWordTrie`) with `build(text)` and `score(word)`, compiled by `setup.py`
into the `trie_matcher` module imported by `002_trie.py`.

The trie is built from the **document text**, with one word per leaf path
(separators: space, newline, comma, tab, CR) and occurrence counts on the
terminal `\0` node — then each keyword is looked up as a single string walk.
This means, faithfully to the original algorithm, **matching is
case-sensitive and only works for single-word keywords**: a multi-word
keyword (e.g. `"Tesla Inc"`) contains a space, which is never a trie edge, so
it always scores 0. This is a direct port, not a fix — `001_naive.py`'s
regex approach remains the correctness baseline.
