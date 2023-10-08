import redis
from redis_lru import RedisLRU

from mongoengine import connect
from uploads import user, passwd, domain, db_name

from models import Author, Quote


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client, default_ttl=180)


def search_by(command, value):
    connect(host=f"mongodb+srv://{user}:{passwd}@{domain}/{db_name}")
    if command == "name":
        a = Author.objects(fullname__icontains=value).first()
        print(a.fullname)
        quote = Quote.objects(author=a.id)
    elif command in ["tag", "tags"]:
        if command == "tag":
            quote = Quote.objects(tags__icontains=value)
        else:
            tags = value.split(",")
            quote = Quote.objects(tags__in=tags)
    else:
        print("\nNot found tag\n")
        return

    for q in quote:
        cache_key = f"{command}:{q.id}"
        if cache.get(cache_key) is None:
            cache.set(cache_key, q.quote)
        print(cache.get(cache_key))
