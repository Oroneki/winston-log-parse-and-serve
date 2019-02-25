from models import LogEntry


def sample_get():
    it = LogEntry.raw('SELECT id from logentry where id % 10000 = 0').execute()
    print(it)
    print([el for el in it])


if __name__ == "__main__":
    sample_get()
