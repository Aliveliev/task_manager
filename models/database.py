import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_file):
        self.conn = self.create_connection(db_file)
        self.create_table()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(self):
        """ create tasks table """
        try:
            sql_create_tasks_table = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                deadline DATETIME,
                priority INTEGER,
                status BOOLEAN
            );
            CREATE INDEX IF NOT EXISTS idx_deadline ON tasks (deadline);
            CREATE INDEX IF NOT EXISTS idx_priority ON tasks (priority);
            """
            c = self.conn.cursor()
            c.executescript(sql_create_tasks_table)
        except Error as e:
            print(e)

    def add_task(self, task):
        """ add a new task """
        sql = ''' INSERT INTO tasks(title, description, deadline, priority, status)
                  VALUES(?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()
        return cur.lastrowid

    def get_tasks(self, limit=None, offset=None):
        """ get all tasks with optional pagination """
        cur = self.conn.cursor()
        sql = "SELECT * FROM tasks"
        if limit is not None and offset is not None:
            sql += " LIMIT ? OFFSET ?"
            cur.execute(sql, (limit, offset))
        else:
            cur.execute(sql)
        rows = cur.fetchall()
        return rows
    
    def get_task(self, task_id):
        """ get a task by task id """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        row = cur.fetchone()
        return row
    
    def get_task_count(self):
        """ get the total number of tasks """
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM tasks")
        count = cur.fetchone()[0]
        return count

    def update_task(self, task):
        """ update a task """
        sql = ''' UPDATE tasks
                  SET title = ? ,
                      description = ? ,
                      deadline = ? ,
                      priority = ? ,
                      status = ?
                  WHERE id = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()

    def delete_task(self, id):
        """ delete a task by task id """
        sql = 'DELETE FROM tasks WHERE id=?'
        cur = self.conn.cursor()
        cur.execute(sql, (id,))
        self.conn.commit()