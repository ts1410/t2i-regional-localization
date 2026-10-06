import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "experiments" / "t2i_research.db"


def get_db_connection():
    os.makedirs(ROOT / "experiments", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(get_db_connection()) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS experiments (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                model TEXT NOT NULL,
                model_version TEXT,
                region TEXT NOT NULL,
                festival TEXT NOT NULL,
                experiment_id TEXT,
                framework_version TEXT,
                framework_hash TEXT,
                campaign_version TEXT,
                campaign_hash TEXT,
                reference_image_hash TEXT,
                prompt_version TEXT,
                generation_parameters TEXT,
                output_path TEXT,
                status TEXT,
                error TEXT,
                provider TEXT,
                api_key_present INTEGER,
                metadata TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS evaluations (
                id TEXT PRIMARY KEY,
                participant_id TEXT NOT NULL,
                experiment_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                responses TEXT NOT NULL,
                comment TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_experiment(record):
    with closing(get_db_connection()) as conn:
        conn.execute(
            """
            INSERT INTO experiments (
                id, timestamp, model, model_version, region, festival, experiment_id,
                framework_version, framework_hash, campaign_version, campaign_hash,
                reference_image_hash, prompt_version, generation_parameters, output_path,
                status, error, provider, api_key_present, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                record["id"],
                record["timestamp"],
                record["model"],
                record.get("model_version"),
                record["region"],
                record["festival"],
                record.get("experiment_id"),
                record.get("framework_version"),
                record.get("framework_hash"),
                record.get("campaign_version"),
                record.get("campaign_hash"),
                record.get("reference_image_hash"),
                record.get("prompt_version"),
                json.dumps(record.get("generation_parameters", {})),
                record.get("output_path"),
                record.get("status"),
                record.get("error"),
                record.get("provider"),
                int(bool(record.get("api_key_present"))),
                json.dumps(record.get("metadata", {})),
            ],
        )
        conn.commit()


def list_experiments():
    with closing(get_db_connection()) as conn:
        rows = conn.execute(
            "SELECT * FROM experiments ORDER BY timestamp DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def get_experiment(experiment_id):
    with closing(get_db_connection()) as conn:
        row = conn.execute(
            "SELECT * FROM experiments WHERE id = ? OR experiment_id = ?",
            (experiment_id, experiment_id),
        ).fetchone()
        if row is None:
            return None
        return dict(row)


def save_evaluation(record):
    with closing(get_db_connection()) as conn:
        conn.execute(
            """
            INSERT INTO evaluations (id, participant_id, experiment_id, timestamp, responses, comment, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                record["id"],
                record["participant_id"],
                record["experiment_id"],
                record["timestamp"],
                json.dumps(record["responses"]),
                record.get("comment"),
                record["created_at"],
            ],
        )
        conn.commit()


def list_evaluations():
    with closing(get_db_connection()) as conn:
        rows = conn.execute(
            "SELECT * FROM evaluations ORDER BY created_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


__all__ = [
    "init_db",
    "save_experiment",
    "get_experiment",
    "list_experiments",
    "save_evaluation",
    "list_evaluations",
]
