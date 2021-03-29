from typing import List

import requests
from typing_extensions import TypedDict

from .defaults import DEFAULT_BOT_LOGS_ENDPOINT


class Log(TypedDict):
    timestamp: int
    severity: str
    log: str


def get_logs(bot_uid: str, uid: str, key: str) -> List[Log]:
    """Retrieves logs for specified bot.

    :param bot_uid:
    :param uid:
    :param key:
    :return:
    """
    r = requests.get(
        DEFAULT_BOT_LOGS_ENDPOINT,
        params={
            'uid': uid,
            'key': key,
            'bot_uid': bot_uid,
        }
    )
    r.raise_for_status()
    return r.json()['data']


def display_logs(logs: List[Log]):
    """Prints logs with clear separation.

    :param logs: Logs retrieved with get_logs()
    :return:
    """
    for log in logs:
        print(f"===== LOG AT {log['timestamp']} (SEVERITY: {log['severity']}) =====")
        print(log['log'])
        print("===== END LOG =====")
