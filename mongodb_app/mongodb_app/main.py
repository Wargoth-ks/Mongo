import sys
import subprocess
import time

from concurrent.futures import ThreadPoolExecutor as pool
from uploads import upload_json
from mongoengine import errors

from pymongo.errors import (
    ConfigurationError as mongodb_error,
    AutoReconnect as reconnect_error,
)

from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import prompt

from docker import run_rabbitmq, run_redis

from search import search_by

history = InMemoryHistory()

def main():
    while True:
        try:
            user_input = prompt(
                "\nEnter command: ", enable_history_search=True, history=history
            )
            if ":" in user_input:
                command, value = user_input.split(":")
                search_by(command.strip(), value.strip())
            else:
                match user_input.strip():
                    case "exit":
                        subprocess.run(["docker", "stop", "redis-cache"])
                        subprocess.run(["docker", "stop", "rabbitmq"])
                        print("Exit program")
                        sys.exit(0)
                    case "upload":
                        upload_json()
                    case "send_mail":
                        time.sleep(5)
                        consumer = subprocess.Popen(["python", "consumer.py"])
                        print("Consumer was starting & waiting ...\n")
                        time.sleep(5)
                        print("Producer starting & sending messages")
                        subprocess.run(["python", "producer.py"])
                        consumer.kill()
                        print("\nDone!")
                    case _:
                        print("\nInvalid command")
        except mongodb_error:
            print(
                "\nFailed connection to database. Please, check you internet connection!\n"
            )
        except reconnect_error:
            print(
                "\nAutoreconnect to database failed. Please, check you internet connection!\n"
            )
        except errors.MongoEngineException as m:
            print(m)
        except AttributeError as a:
            print(a)
        except KeyboardInterrupt:
            subprocess.run(["docker", "stop", "redis-cache"])
            subprocess.run(["docker", "stop", "rabbitmq"])
            break


if __name__ == "__main__":
    with pool() as executor:
        thr_docker = executor.submit(run_redis)
        thr_rabbit = executor.submit(run_rabbitmq)
        time.sleep(3)
        thr_main = executor.submit(main)
