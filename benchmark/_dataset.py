import json
import os

import psycopg2
import psycopg2.extras

DATASET_SIZE = 2 ** 12
DATASET_FILE = os.path.join(os.path.dirname(__file__), "data", "tsla_articles.json")
KEYWORDS_FILE = os.path.join(os.path.dirname(__file__), "keywords_tsla.txt")
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
)


def download_dataset():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, text FROM articles ORDER BY id LIMIT %s", (DATASET_SIZE,))
    rows = cur.fetchall()
    cur.close()
    conn.close()

    os.makedirs(os.path.dirname(DATASET_FILE), exist_ok=True)
    with open(DATASET_FILE, "w") as f:
        json.dump([{"id": str(row["id"]), "text": row["text"] or ""} for row in rows], f)


def load_dataset():
    if not os.path.exists(DATASET_FILE):
        download_dataset()
    with open(DATASET_FILE, "r") as f:
        return json.load(f)


def load_keywords():
    return open(KEYWORDS_FILE, "r").read().strip().split("\n")
