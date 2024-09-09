import os
import sys
import django
# Тут ми підключаємся до дж орм із за меж джанго -------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quotes.settings")
django.setup()
# ------------------------------------------------------------------------------
from app_quotes.models import Author, Quote, Tag


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def connect_mongobd():
    uri = "mongodb+srv://admin:12345@cluster0.aw3ob.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return client["test"]

db = connect_mongobd()

def authors_migrate():
    """ Migrate authors """
    authors = db['authors'].find()
    
    for auth in authors:
        if not Author.objects.filter(fullname = auth['fullname']).exists():
            author = Author(fullname = auth['fullname'], 
                            born_date = auth['born_date'],
                            born_location = auth['born_location'],
                            description = auth['description'])
            author.save()
            print(f"Add author: {auth['fullname']}")
    print(" You successfully migrate authors!")


def quotes_quotes():
    """ Migrate quotes """
    quotes = db['quotes'].find()
    
    for q in quotes:
        
        # ==== Перевірка всіх тегів цитати на існування, якщо ні тоді створює.
        tags = []
        for tag in q['tags']:
            t, *_ = Tag.objects.get_or_create(name=tag)
            tags.append(t)

        if not Quote.objects.filter(quote = q['quote']).exists():

            author_from_mongo = db.authors.find_one({"_id": q["owner"]})
        
            author_to_postgre = Author.objects.get(fullname=author_from_mongo["fullname"])

            quote = Quote(quote = q['quote'], owner = author_to_postgre)    # Ств цитату
            quote.save()         #  Зберігаєм цитату
            for tag in tags:
                quote.tags.add(tag)   # Додаєм теги до цитати

            print(f"Add quote: {author_from_mongo['fullname']} - {quote}")
    print(" You successfully migrate quotes!")

if __name__=="__main__":
    authors_migrate()
    quotes_quotes()