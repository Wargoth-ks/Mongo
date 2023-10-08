import subprocess

def run_redis():
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--name",
            "redis-cache",
            "-p",
            "6379:6379",
            "-d",
            "redis",
        ]
    )
    
    print(f"Start redis")

def run_rabbitmq():
    subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "-d",
            "--name",
            "rabbitmq",
            "-p",
            "5672:5672",
            "-p",
            "15672:15672",
            "rabbitmq:alpine",
        ]
    )
    print(f"Start rabbitmq")