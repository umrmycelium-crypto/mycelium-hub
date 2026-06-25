import sqlite3
import json
import time

DB = "mycelium_events.db"


def init():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            event TEXT,
            payload TEXT
        )
    """)
    conn.commit()
    conn.close()


def append_event(event: dict):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "INSERT INTO events (timestamp, event, payload) VALUES (?, ?, ?)",
        (
            time.time(),
            event.get("event", "unknown"),
            json.dumps(event.get("payload", {}))
        )
    )

    conn.commit()
    conn.close()


def read_events(limit: int = 100):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute(
        "SELECT timestamp, event, payload FROM events ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    rows = c.fetchall()
    conn.close()

    return [
        {
            "timestamp": r[0],
            "event": r[1],
            "payload": json.loads(r[2])
        }
        for r in rows[::-1]
    ]


def system_event_db(payload, context):
    return {
        "status": "OK",
        "events": len(read_events(50))
    }


init()
