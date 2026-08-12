import os
import sqlite3
import json
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.core.config import settings

class MemoryService:
    def __init__(self, db_path: str = settings.SQLITE_DB_PATH):
        self.db_path = db_path
        self.json_backup_path = os.path.join(os.path.dirname(self.db_path), "chat_history.json")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
        self._restore_from_json_if_needed()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            # Session Metadata table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    destination TEXT,
                    duration TEXT,
                    language TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def _restore_from_json_if_needed(self):
        """If SQLite DB is empty on startup, restore chat history from chat_history.json file."""
        if not os.path.exists(self.json_backup_path):
            return
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM messages")
                count = cursor.fetchone()[0]
                if count == 0:
                    with open(self.json_backup_path, "r", encoding="utf-8") as f:
                        history_data = json.load(f)
                        if isinstance(history_data, list):
                            for sess in history_data:
                                sid = sess.get("session_id")
                                msgs = sess.get("messages", [])
                                for m in msgs:
                                    role = m.get("role") or m.get("sender") or "user"
                                    if role == "ai":
                                        role = "assistant"
                                    content = m.get("content") or m.get("message") or ""
                                    if sid and content:
                                        cursor.execute(
                                            "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
                                            (sid, role, content)
                                        )
                                cursor.execute(
                                    "INSERT OR REPLACE INTO sessions (session_id, updated_at) VALUES (?, CURRENT_TIMESTAMP)",
                                    (sid,)
                                )
                            conn.commit()
                            print(f"MemoryService: Restored {len(history_data)} chat sessions from {self.json_backup_path}")
        except Exception as e:
            print(f"MemoryService JSON restore note: {e}")

    def _sync_to_json_file(self):
        """Export all chat sessions and messages to storage/conversations/chat_history.json file."""
        try:
            sessions = self.get_all_sessions()
            full_history = []
            for s in sessions:
                sid = s["session_id"]
                msgs = self.get_history(sid, limit=200)
                full_history.append({
                    "session_id": sid,
                    "title": s["title"],
                    "updated_at": s["updated_at"],
                    "message_count": s["message_count"],
                    "messages": msgs
                })
            with open(self.json_backup_path, "w", encoding="utf-8") as f:
                json.dump(full_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"MemoryService JSON sync note: {e}")

    def get_or_create_session_id(self, session_id: Optional[str] = None) -> str:
        if not session_id or not session_id.strip():
            return f"session_{uuid.uuid4().hex[:8]}"
        return session_id.strip()

    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            meta_json = json.dumps(metadata) if metadata else None
            cursor.execute(
                "INSERT INTO messages (session_id, role, content, metadata) VALUES (?, ?, ?, ?)",
                (session_id, role, content, meta_json)
            )
            # Update session timestamp
            cursor.execute(
                "INSERT INTO sessions (session_id, updated_at) VALUES (?, CURRENT_TIMESTAMP) ON CONFLICT(session_id) DO UPDATE SET updated_at=CURRENT_TIMESTAMP",
                (session_id,)
            )
            conn.commit()
        self._sync_to_json_file()


    def update_session_metadata(self, session_id: str, destination: Optional[str] = None, duration: Optional[str] = None, language: Optional[str] = None):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT destination, duration, language FROM sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            
            cur_dest = destination or (row[0] if row else None)
            cur_dur = duration or (row[1] if row else None)
            cur_lang = language or (row[2] if row else None)
            
            cursor.execute("""
                INSERT INTO sessions (session_id, destination, duration, language, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(session_id) DO UPDATE SET
                    destination = COALESCE(excluded.destination, sessions.destination),
                    duration = COALESCE(excluded.duration, sessions.duration),
                    language = COALESCE(excluded.language, sessions.language),
                    updated_at = CURRENT_TIMESTAMP
            """, (session_id, cur_dest, cur_dur, cur_lang))
            conn.commit()

    def get_session_metadata(self, session_id: str) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT destination, duration, language FROM sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            if row:
                return {"destination": row[0], "duration": row[1], "language": row[2]}
            return {}

    def get_history(self, session_id: str, limit: int = settings.MAX_HISTORY_MESSAGES) -> List[Dict[str, str]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, content FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
                (session_id, limit)
            )
            rows = cursor.fetchall()
            # Return in chronological order
            return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

    def delete_session(self, session_id: str) -> bool:
        sid = session_id.strip()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages WHERE session_id = ? OR session_id = ? OR session_id = ?", (sid, f"#{sid}", sid.lstrip("#")))
            cursor.execute("DELETE FROM sessions WHERE session_id = ? OR session_id = ? OR session_id = ?", (sid, f"#{sid}", sid.lstrip("#")))
            conn.commit()
        self._sync_to_json_file()
        return True

    def delete_all_sessions(self) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM messages")
            cursor.execute("DELETE FROM sessions")
            conn.commit()
        self._sync_to_json_file()
        return True


    def get_all_sessions(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    m.session_id, 
                    MAX(m.created_at) as last_updated, 
                    COUNT(m.id) as message_count,
                    (SELECT content FROM messages WHERE session_id = m.session_id AND role = 'user' ORDER BY id ASC LIMIT 1) as first_user_msg
                FROM messages m
                GROUP BY m.session_id
                ORDER BY last_updated DESC
            """)
            rows = cursor.fetchall()
            
            sessions = []
            for r in rows:
                sid, last_updated, msg_count, raw_title = r[0], r[1], r[2], r[3]
                title = "New Chat"
                if raw_title and raw_title.strip():
                    clean_t = " ".join(raw_title.strip().split())
                    title = clean_t[:45] + ("..." if len(clean_t) > 45 else "")
                
                sessions.append({
                    "session_id": sid,
                    "updated_at": last_updated,
                    "message_count": msg_count,
                    "title": title
                })
            return sessions


memory_service = MemoryService()
