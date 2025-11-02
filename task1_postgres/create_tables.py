import psycopg2
from psycopg2 import sql

DB_NAME = "tasks_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
"""

create_status_table = """
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
"""

create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""

def main():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(create_users_table)
        cur.execute(create_status_table)
        cur.execute(create_tasks_table)

        insert_statuses = """
        INSERT INTO status (name) VALUES
            ('new'),
            ('in progress'),
            ('completed')
        ON CONFLICT (name) DO NOTHING;
        """
        cur.execute(insert_statuses)

        print("Таблиці створені, статуси додані.")
        cur.close()
    except Exception as e:
        print("Помилка під час створення таблиць:", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
