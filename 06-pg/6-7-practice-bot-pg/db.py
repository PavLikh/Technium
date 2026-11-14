from sqlite3 import connect, Row
from datetime import datetime, timedelta


USERS_TABLE = 'users'
SLEEP_RECORDS_TABLE = 'sleep_records'
NOTES_TABLE = 'notes'
TABLE_SCHEMAS = {
    USERS_TABLE: """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT
        );
    """,
    SLEEP_RECORDS_TABLE: """
        CREATE TABLE IF NOT EXISTS sleep_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            sleep_time DATETIME DEFAULT NULL,
            wake_time DATETIME DEFAULT NULL,
            sleep_quality INTEGER DEFAULT NULL,
            FOREIGN KEY ("user_id") REFERENCES "users" ("id")
        );
    """,
    NOTES_TABLE: """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            sleep_record_id INTEGER NOT NULL,
            FOREIGN KEY ("sleep_record_id") REFERENCES "sleep_records" ("id")
        );
    """,
}

ALLOWED_TABLES = set(TABLE_SCHEMAS.keys())

def _is_int(value) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)

class DataBase:
    def __init__(self):
        try:
            self.conn = connect("telebot.db", check_same_thread=False)
            self.conn.row_factory = Row
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.init_tables()
            print("Connect to SQLite successful")

        except Exception as e:
            print('Connection failure:', e)
            raise
    
    def init_tables(self):
        cur = self.conn.cursor()
        for schema in TABLE_SCHEMAS.values():
            cur.execute(schema)
        self.conn.commit()
        cur.close()
    
    def close_connect(self) -> None:
        self.conn.close()


class Table():
    def __init__(self, name: str, db: DataBase):
        if name not in ALLOWED_TABLES:
            raise ValueError(f"Wrong table: {name}")
        self.name = name
        self.db = db

    @property
    def conn(self):
        return self.db.conn

    def is_exists(self, id: int) -> bool:
        if not _is_int(id):
            return False
    
        query = f"SELECT 1 FROM {self.name} WHERE id = ? LIMIT 1"
        cur = self.conn.cursor()
        try:
            cur.execute(query, (id,))
            return cur.fetchone() is not None
        finally:
            cur.close()

    def get_columns(self) -> set:
        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT * FROM {self.name} LIMIT 0")
            return {col[0] for col in cur.description}
        finally:
            cur.close()


    def get_required_columns(self) -> set:
        required = set()
        cur = self.conn.cursor()
        try:
            cur.execute(f"PRAGMA table_info({self.name})")
            for _, name, _, notnull, dflt_value, pk in cur.fetchall():
                if pk:
                    continue
                if notnull and dflt_value is None:
                    required.add(name)
        finally:
            cur.close()
        return required
    
    def insert_row(self, data) -> None:
        if 'id' in data and  _is_int(data['id']):
            row_id = data['id']
        elif self.name == USERS_TABLE:
            print('Invalid or missing id for users')
            return
        else:
            row_id = None

        if row_id is not None and self.is_exists(row_id):
            print(f"Row with id: {row_id} already exists")
            return

        columns = self.get_columns()
        required = self.get_required_columns()

        missing = required - set(data.keys())
        if missing:
            print(f"Missing required fields: {', '.join(sorted(missing))}")
            return

        cols = [c for c in columns if c in data]
        if not cols:
            print('Nothing to insert: no valid fields in data')
            return

        placeholders = ', '.join('?' for _ in cols)
        values = [data[c] for c in cols]
        cur = self.conn.cursor()
        try:
            cur.execute(
                f"INSERT INTO {self.name} ({', '.join(cols)}) VALUES ({placeholders})",
                values
            )
            new_id = cur.lastrowid
            self.conn.commit()
            print(f"Row: {new_id} added successful")
        except Exception as e:
            self.conn.rollback()
            print(f"Unexpected error during insert: {e}")
        finally:
            cur.close()

    def update_row(self, data) -> None:
        if 'id' in data and _is_int(data['id']):
            row_id = data['id']
            if not self.is_exists(row_id):
                print(f'Error: Row {row_id} not found')
                return
        else:
            print('Error: Invalid or missing id')
            return

        columns = self.get_columns()
        cols = [c for c in columns if c in data and c != 'id']
        if not cols:
            print('Warning: Nothing to update')
            return

        set_part = ', '.join(f'{c} = ?' for c in cols)
        values = [data[c] for c in cols] + [row_id]
        cur = self.conn.cursor()
        try:
            cur.execute(f'UPDATE {self.name} SET {set_part} WHERE id = ?', values)
            rowcount = cur.rowcount
            self.conn.commit()
            if rowcount == 0:
                print(f'Warning: Row {row_id} not updated')
                return
            print(f'Success: Row {row_id} updated')
        except Exception as e:
            self.conn.rollback()
            print(f'Error: Update failed: {e}')
        finally:
            cur.close()

        
    def get_rows(self, limit: int) -> list[Row]:
        if not _is_int(limit):
            raise ValueError("limit must be int")

        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT * FROM {self.name} LIMIT ?", (limit,))
            return cur.fetchall()
        finally:
            cur.close()

    
    def get_row(self, row_id: int) -> Row | None:
        if not _is_int(row_id):
            raise ValueError(f"Invalid row_id type: expected int, got {type(row_id).__name__}")
        
        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT * FROM {self.name} WHERE id = ?", (row_id,))
            return cur.fetchone()
        finally:
            cur.close()

class Users(Table):
    def __init__(self, db: DataBase):
        super().__init__(USERS_TABLE, db)

    def ensure_exists(self, user_id: int, name: str | None = None) -> None:
        if self.is_exists(user_id):
            return
        
        self.insert_row({
            "id": user_id,
            "name": name
        })

class SleepRecords(Table):
    def __init__(self, db: DataBase):
        super().__init__(SLEEP_RECORDS_TABLE, db)
   
    def get_last_sleep(self, user_id: int) -> Row | None:
        if not _is_int(user_id):
            raise ValueError(f"Invalid row_id type: expected int, got {type(user_id).__name__}")

        query = f"""
            SELECT * FROM {self.name}
            WHERE user_id = ?
            ORDER BY sleep_time DESC
            LIMIT 1
        """
        cur = self.conn.cursor()
        try:
            return cur.execute(query, (user_id,)).fetchone()
        finally:
            cur.close()

    def get_is_active(self, user_id: int) -> Row | None:
        if not _is_int(user_id):
            raise ValueError(f"Invalid row_id type: expected int, got {type(user_id).__name__}")

        sleep = self.get_last_sleep(user_id)
        if sleep is None or sleep['wake_time'] is not None:
            return None

        return sleep
    
    def get_is_completed(self, user_id: int) -> Row | None:
        if not _is_int(user_id):
            raise ValueError(f"Invalid row_id type: expected int, got {type(user_id).__name__}")

        sleep = self.get_last_sleep(user_id)
        if sleep is None or sleep['wake_time'] is None:
            return None

        return sleep

    def get_all_for_user(self, user_id: int) -> list[Row]:
        if not _is_int(user_id):
            raise ValueError(f"Invalid user_id type: expected int, got {type(user_id).__name__}")

        query = f"""
            SELECT * FROM {self.name}
            WHERE user_id = ?
        """
        cur = self.conn.cursor()
        try:
            return cur.execute(query, (user_id,)).fetchall()
        finally:
            cur.close()


class Notes(Table):
    def __init__(self, db: DataBase):
        super().__init__(NOTES_TABLE, db)

    def get_note(self, sleep_record_id: int):
        if not _is_int(sleep_record_id):
            raise ValueError(f"Invalid sleep_id type: expected int, got {type(sleep_record_id).__name__}")

        query = f"""
            SELECT * FROM {self.name}
            WHERE sleep_record_id = ?
            LIMIT 1
        """
        cur = self.conn.cursor()
        try:
            return cur.execute(query, (sleep_record_id,)).fetchone()
        finally:
            cur.close()
