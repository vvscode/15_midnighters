import requests
import pytz
from datetime import datetime


def get_attempt_hour(attempt):
    local_date = datetime.fromtimestamp(
        attempt["timestamp"],
        pytz.timezone(attempt["timezone"])
    )
    return local_date.hour


def load_attempts():
    page_number = 1
    number_of_pages = 1
    url = "https://devman.org/api/challenges/solution_attempts/"
    while page_number <= number_of_pages:
        page_content = requests.get(url, params={
            "page": page_number
        }).json()

        attemps = page_content["records"]
        number_of_pages = page_content["number_of_pages"]

        page_number += 1

        for attempt in attemps:
            yield attempt


def get_midnighters_attempts(attempts):
    new_day_hour = 6
    return filter(lambda x: get_attempt_hour(x) < new_day_hour, attempts)


def get_usernames_from_attempts(attempts):
    names = map(lambda x: x["username"], attempts)
    return list(set(names))


if __name__ == "__main__":
    attemps = load_attempts()
    usernames = get_usernames_from_attempts(get_midnighters_attempts(attemps))
    print("{} midnighter(s) detected".format(len(usernames)))
