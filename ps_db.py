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


