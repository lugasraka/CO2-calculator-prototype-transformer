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

            CREATE TABLE IF NOT EXISTS module2_eol (
                eol_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                total_portfolio_kt REAL NOT NULL,
                total_units   INTEGER NOT NULL,
                volumes_json  TEXT    NOT NULL,
                created_at    TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS app_preference (
                key           TEXT PRIMARY KEY,
                value         TEXT NOT NULL,
                updated_at    TEXT NOT NULL
            );
            """
        )


def save_run(
    name: str, choices: dict, volumes: dict, kpis: dict, results: pd.DataFrame
) -> int:
    """Persist a scenario + its simulation run. Returns the new run_id."""
    init_db()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect() as conn:
        cur = conn.execute(
            """INSERT INTO scenario
               (name, core_choice, fluid_choice, copper_choice,
                vol_dist, vol_med, vol_large, created_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (
                name,
                choices["core"],
                choices["fluid"],
                choices["copper"],
                volumes["dist"],
                volumes["med"],
                volumes["large"],
                now,
            ),
        )
        scenario_id = cur.lastrowid
        cur = conn.execute(
            """INSERT INTO simulation_run
               (scenario_id, total_base, total_eco, total_saving,
                pct_saving, results_json, created_at)
               VALUES (?,?,?,?,?,?,?)""",
            (
                scenario_id,
                kpis["total_base"],
                kpis["total_eco"],
                kpis["total_saving"],
                kpis["pct_saving"],
                results.to_json(orient="records"),
                now,
            ),
        )
        return cur.lastrowid  # type: ignore[return-value]


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


def get_latest_run() -> tuple[pd.Series | None, pd.DataFrame]:
    """Return the most recent saved run plus its per-family results.

    Returns ``(None, empty_df)`` when no run has been saved yet.
    Powers Module 4's Scope 3.1 reporting so it survives tab refresh, multi-tab
    and mobile views (no longer coupled to Streamlit session state).
    """
    init_db()
    with _connect() as conn:
        row = conn.execute(
            """SELECT r.run_id, s.name, s.created_at,
                      s.core_choice, s.fluid_choice, s.copper_choice,
                      s.vol_dist, s.vol_med, s.vol_large,
                      r.total_base, r.total_eco, r.total_saving, r.pct_saving
               FROM simulation_run r
               JOIN scenario s ON s.scenario_id = r.scenario_id
               ORDER BY r.run_id DESC
               LIMIT 1"""
        ).fetchone()
    if row is None:
        return None, pd.DataFrame()
    return row, get_run_results(int(row["run_id"]))


def save_module2_eol(total_portfolio_kt: float, total_units: int, volumes: dict) -> int:
    """Persist Module 2's decommissioning-branch output for Module 4 retrieval.

    Each call inserts a new row; ``get_latest_module2_eol`` returns the newest.
    Mirrors the session-state ``mod2_eol`` shape in ``app.py``.
    """
    init_db()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect() as conn:
        cur = conn.execute(
            """INSERT INTO module2_eol
               (total_portfolio_kt, total_units, volumes_json, created_at)
               VALUES (?,?,?,?)""",
            (total_portfolio_kt, total_units, json.dumps(volumes), now),
        )
        return cur.lastrowid  # type: ignore[return-value]


def get_latest_module2_eol() -> dict | None:
    """Return the most recent Module 2 EOL output, or ``None`` if none saved."""
    init_db()
    with _connect() as conn:
        row = conn.execute(
            """SELECT total_portfolio_kt, total_units, volumes_json, created_at
               FROM module2_eol
               ORDER BY eol_id DESC
               LIMIT 1"""
        ).fetchone()
    if row is None:
        return None
    return {
        "total_portfolio_kt": float(row["total_portfolio_kt"]),
        "total_units": int(row["total_units"]),
        "volumes": json.loads(row["volumes_json"]),
        "created_at": row["created_at"],
    }


def set_preference(key: str, value: str) -> None:
    """Upsert a single string preference (e.g. last-used cost ceiling)."""
    init_db()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect() as conn:
        conn.execute(
            """INSERT INTO app_preference (key, value, updated_at)
               VALUES (?,?,?)
               ON CONFLICT(key) DO UPDATE SET value=excluded.value,
                                               updated_at=excluded.updated_at""",
            (key, value, now),
        )


def get_preference(key: str) -> str | None:
    """Read a single string preference; ``None`` if never set."""
    init_db()
    with _connect() as conn:
        row = conn.execute(
            "SELECT value FROM app_preference WHERE key = ?", (key,)
        ).fetchone()
    return None if row is None else str(row["value"])
