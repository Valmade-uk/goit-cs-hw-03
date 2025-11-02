import random
from faker import Faker
import psycopg2

DB_NAME = "tasks_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"

fake = Faker()

USERS_COUNT = 10
TASKS_COUNT = 30

def get_status_ids(cur):
    cur.execute("SELECT id FROM status;")
    rows = cur.fetchall()
    return [row[0] for row in rows]

def get_user_ids(cur):
    cur.execute("SELECT id FROM users;")
    rows = cur.fetchall()
    return [row[0] for row in rows]

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

        for _ in range(USERS_COUNT):
            fullname = fake.name()
            email = fake.unique.email()
            cur.execute(
                "INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING;",
                (fullname, email),
            )

        user_ids = get_user_ids(cur)
        status_ids = get_status_ids(cur)

        for _ in range(TASKS_COUNT):
            title = fake.sentence(nb_words=4)
            description = fake.text(max_nb_chars=200)
            status_id = random.choice(status_ids)
            user_id = random.choice(user_ids)
            cur.execute(
                """
                INSERT INTO tasks (title, description, status_id, user_id)
                VALUES (%s, %s, %s, %s);
                """,
                (title, description, status_id, user_id),
            )

        print("Дані успішно додані.")
        cur.close()
    except Exception as e:
        print("Помилка при наповненні:", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
