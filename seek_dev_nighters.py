import requests
import pytz
import datetime
import copy


def extend_attempt_with_local_time(attempt):
    extended_attempt = copy.copy(attempt)

    utc_date = datetime.datetime.utcfromtimestamp(attempt["timestamp"])
    timezone = pytz.timezone(attempt["timezone"])
    local_date = utc_date.replace(tzinfo=timezone)

    extended_attempt["local_hour"] = local_date.hour
    return extended_attempt


def load_attempts():
    page_number = 1
    number_of_pages = 1
    url = "https://devman.org/api/challenges/solution_attempts/"
    while page_number <= number_of_pages:
        page_content = requests.get(url, params = {
            "page": page_number
        }).json()

        attemps = page_content["records"]
        number_of_pages = page_content["number_of_pages"]

        page_number += 1

        for attempt in attemps:
            yield extend_attempt_with_local_time(attempt)


def get_midnighters(attempts):
    new_day_hour = 6
    return filter(lambda x: x["local_hour"] < new_day_hour, attempts)


def get_usernames_from_attempts(attempts):
    names = map(lambda x: x["username"], attempts)
    return list(set(names))


if __name__ == "__main__":
    attemps = load_attempts()
    usernames = get_usernames_from_attempts(get_midnighters(attemps))
    print("{} midnighter(s) detected".format(len(usernames)))
