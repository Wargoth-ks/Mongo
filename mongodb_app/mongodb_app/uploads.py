import json
import configparser

from mongoengine import connect

from pathlib import Path
from models import Author, Quote

config = configparser.ConfigParser()
config.read("config.ini")

user = config.get("DB", "user")
passwd = config.get("DB", "passwd")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

connect(host=f"mongodb+srv://{user}:{passwd}@{domain}/{db_name}")

js_path = Path("json_files")

authors_path = js_path.joinpath("authors.json")
quotes_path = js_path.joinpath("quotes.json")


def upload_json():
    try:
        with open(authors_path, "r", encoding="utf-8") as file_1, open(
            quotes_path, "r", encoding="utf-8"
        ) as file_2:
            js_1 = file_1.read()
            js_2 = file_2.read()
            authors_data = json.loads(js_1)
            quotes_data = json.loads(js_2)

        for authors in authors_data:
            print(authors)
            Author(**authors).save()
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data["author"]).first()
            if author:
                quote = Quote(
                    tags=quote_data["tags"], author=author, quote=quote_data["quote"]
                )
                print(quote)
                quote.save()
    except json.JSONDecodeError as jserr:
        print(jserr)


if __name__ == "__main__":
    upload_json()
