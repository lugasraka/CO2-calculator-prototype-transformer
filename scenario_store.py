"""Scenario & simulation-run persistence (Phase 1).

Makes scenarios first-class: a *scenario* is a named set of Scenario-B design
choices plus the volume forecast it was run against; a *simulation_run* records
the computed portfolio results so runs can be saved, listed, compared and
exported instead of vanishing on rerun.

Backed by a local SQLite file (``data/runs.db``). The relational shape here is
the Phase-1 seed of the ``scenario`` / ``simulation_run`` schema that Phase 2+
grows into (owners, temporal validity, audit trail).
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).parent / "data" / "runs.db"

# Categories persisted as scenario design choices (Scenario A baseline is implicit).
CHOICE_KEYS = ["core", "fluid", "copper"]


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the scenario/run tables if they do not yet exist."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS scenario (
                scenario_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                core_choice   TEXT    NOT NULL,
                fluid_choice  TEXT    NOT NULL,
                copper_choice TEXT    NOT NULL,
                vol_dist      INTEGER NOT NULL,
                vol_med       INTEGER NOT NULL,
                vol_large     INTEGER NOT NULL,
                created_at    TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS simulation_run (
                run_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_id   INTEGER NOT NULL REFERENCES scenario(scenario_id),
                total_base    REAL    NOT NULL,
                total_eco     REAL    NOT NULL,
                total_saving  REAL    NOT NULL,
                pct_saving    REAL    NOT NULL,
                results_json  TEXT    NOT NULL,
                created_at    TEXT    NOT NULL
            );
            """
        )


def save_run(name: str, choices: dict, volumes: dict, kpis: dict,
             results: pd.DataFrame) -> int:
    """Persist a scenario + its simulation run. Returns the new run_id."""
    init_db()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect() as conn:
        cur = conn.execute(
            """INSERT INTO scenario
               (name, core_choice, fluid_choice, copper_choice,
                vol_dist, vol_med, vol_large, created_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (name, choices["core"], choices["fluid"], choices["copper"],
             volumes["dist"], volumes["med"], volumes["large"], now),
        )
        scenario_id = cur.lastrowid
        cur = conn.execute(
            """INSERT INTO simulation_run
               (scenario_id, total_base, total_eco, total_saving,
                pct_saving, results_json, created_at)
               VALUES (?,?,?,?,?,?,?)""",
            (scenario_id, kpis["total_base"], kpis["total_eco"],
             kpis["total_saving"], kpis["pct_saving"],
             results.to_json(orient="records"), now),
        )
        return cur.lastrowid


def list_runs() -> pd.DataFrame:
    """Saved runs (newest first) joined with their scenario for the picker/compare."""
    init_db()
    with _connect() as conn:
        return pd.read_sql_query(
            """SELECT r.run_id, s.name, s.created_at,
                      s.core_choice, s.fluid_choice, s.copper_choice,
                      s.vol_dist, s.vol_med, s.vol_large,
                      r.total_base, r.total_eco, r.total_saving, r.pct_saving
               FROM simulation_run r
               JOIN scenario s ON s.scenario_id = r.scenario_id
               ORDER BY r.run_id DESC""",
            conn,
        )


def get_run_results(run_id: int) -> pd.DataFrame:
    """Rehydrate the per-family results table stored with a run."""
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT results_json FROM simulation_run WHERE run_id = ?", (run_id,)
        ).fetchone()
    if row is None:
        return pd.DataFrame()
    return pd.DataFrame(json.loads(row["results_json"]))


def delete_run(run_id: int) -> None:
    """Remove a run and its (now-orphaned) scenario."""
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT scenario_id FROM simulation_run WHERE run_id = ?", (run_id,)
        ).fetchone()
        conn.execute("DELETE FROM simulation_run WHERE run_id = ?", (run_id,))
        if row is not None:
            conn.execute(
                "DELETE FROM scenario WHERE scenario_id = ?", (row["scenario_id"],)
            )
