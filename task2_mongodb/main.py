import urllib.parse
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError

load_dotenv()

USERNAME = os.getenv("MONGO_USERNAME")
RAW_PASSWORD = os.getenv("MONGO_PASSWORD")
CLUSTER_HOST = os.getenv("MONGO_CLUSTER_HOST")
APP_NAME = os.getenv("MONGO_APP_NAME", "app")

ENCODED_PASSWORD = urllib.parse.quote_plus(RAW_PASSWORD)

MONGO_URI = (
    f"mongodb+srv://{USERNAME}:{ENCODED_PASSWORD}"
    f"@{CLUSTER_HOST}/?retryWrites=true&w=majority&appName={APP_NAME}")

DB_NAME = "cats_db"
COLLECTION_NAME = "cats"

def get_collection():
    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))
    db = client[DB_NAME]
    return db[COLLECTION_NAME]


# ------------ CREATE ------------
def create_cat(name: str, age: int, features: list[str]):
    collection = get_collection()
    try:
        result = collection.insert_one(
            {
                "name": name,
                "age": age,
                "features": features
            }
        )
        print(f"Кота створено з _id = {result.inserted_id}")
    except PyMongoError as e:
        print("Помилка при створенні:", e)


# ------------ READ ------------
def read_all():
    collection = get_collection()
    try:
        docs = list(collection.find())
        if not docs:
            print("Колекція порожня.")
        for doc in docs:
            print(doc)
    except PyMongoError as e:
        print("Помилка при читанні всіх:", e)


def read_by_name(name: str):
    collection = get_collection()
    try:
        doc = collection.find_one({"name": name})
        if doc:
            print(doc)
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except PyMongoError as e:
        print("Помилка при читанні за ім'ям:", e)


# ------------ UPDATE ------------
def update_age(name: str, new_age: int):
    collection = get_collection()
    try:
        result = collection.update_one(
            {"name": name},
            {"$set": {"age": new_age}}
        )
        if result.matched_count == 0:
            print(f"Кота '{name}' не знайдено.")
        else:
            print(f"Вік кота '{name}' оновлено до {new_age}.")
    except PyMongoError as e:
        print("Помилка при оновленні віку:", e)


def add_feature(name: str, feature: str):
    collection = get_collection()
    try:
        result = collection.update_one(
            {"name": name},
            {"$addToSet": {"features": feature}}  # не додає дублі
        )
        if result.matched_count == 0:
            print(f"Кота '{name}' не знайдено.")
        else:
            print(f"Характеристику '{feature}' додано коту '{name}'.")
    except PyMongoError as e:
        print("Помилка при додаванні характеристики:", e)


# ------------ DELETE ------------
def delete_by_name(name: str):
    collection = get_collection()
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count == 0:
            print(f"Кота '{name}' не знайдено.")
        else:
            print(f"Кота '{name}' видалено.")
    except PyMongoError as e:
        print("Помилка при видаленні:", e)


def delete_all():
    collection = get_collection()
    try:
        result = collection.delete_many({})
        print(f"Видалено документів: {result.deleted_count}")
    except PyMongoError as e:
        print("Помилка при видаленні всіх:", e)


if __name__ == "__main__":
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])

    print("\n--- всі коти ---")
    read_all()

    print("\n--- пошук barsik ---")
    read_by_name("barsik")

    print("\n--- оновлення віку barsik ---")
    update_age("barsik", 4)

    print("\n--- додавання фічі ---")
    add_feature("barsik", "любить їсти")

    print("\n--- ще раз прочитаємо barsik ---")
    read_by_name("barsik")

    # нижче дві “небезпечні” операції — краще викликати вручну:
    # delete_by_name("barsik")
    # delete_all()
