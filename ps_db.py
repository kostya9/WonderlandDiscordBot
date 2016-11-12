import psycopg2 as ps
import os
import urllib.parse;

OS_DB_VAR_NAME = "DATABASE_URL"

class psdb:
    def __init__(self):
        db_name = str(os.environ[OS_DB_VAR_NAME])
        parsed_url = urllib.parse.urlparse(db_name)
        self.conn = ps.connect(
            database=parsed_url.path[1:],
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.hostname,
            port=parsed_url.port)
        if self.conn is not None:
            print("Connection with db was established")
        else:
            raise ConnectionError('Could not connect to db')

        self._init_jinxed()
        self._init_commands_messages()

    def _init_jinxed(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS commands (
        name varchar(40) NOT NULL PRIMARY KEY,
        times integer NOT NULL
        );
        """)

        cursor.execute("""
        INSERT INTO commands (name, times) VALUES ('jinxed', 0) ON CONFLICT DO NOTHING;
        """)

    def _init_commands_messages(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS commands_messages (
        name varchar(40) NOT NULL PRIMARY KEY,
        message VARCHAR(100) NOT NULL
        );
        """)
        self.conn.commit()

    def add_message(self, name, message):
        cursor = self.conn.cursor()
        data = (name, message)
        cursor.execute("""
        INSERT INTO commands_messages (name, message) VALUES (%s, %s) ON CONFLICT DO NOTHING;
        """, data)
        self.conn.commit()

    def delete_message(self, name):
        cursor = self.conn.cursor()
        cursor.execute("""
        DELETE  FROM commands_messages WHERE name=%s;
        """, (name,))
        self.conn.commit()

    def increase_jinxed(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE commands SET times = times + 1 WHERE name='jinxed';
        """)
        self.conn.commit();

    def get_jinxed_times(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT commands.times FROM commands WHERE name='jinxed';
        """)
        rows = cursor.fetchall()
        times = rows[0][0]
        return times

    def get_message(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT commands_messages.message FROM commands_messages WHERE name=%s;", (name,))
        fetched = cursor.fetchall()
        if len(fetched) < 1:
            return None
        result = fetched[0][0]
        return result

    def get_all_messages(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT commands_messages.name FROM commands_messages")
        messages = cursor.fetchall()
        return [s[0] for s in messages]


