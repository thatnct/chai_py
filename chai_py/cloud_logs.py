import sys
from datetime import datetime
from typing import List

import requests
from typing_extensions import TypedDict

from .auth import get_auth
from .defaults import DEFAULT_BOT_LOGS_ENDPOINT
from .logger import logger


class Log(TypedDict):
    timestamp: int
    severity: str
    log: str


def get_logs(bot_uid: str, errors: bool = False) -> List[Log]:
    """Retrieves logs for specified bot.

    Logs can only be pulled by the bot's developer.

    :param bot_uid: Bot UID
    :param errors: If True, only retrieves logs with severity: Error
    :return:
    """
    auth = get_auth()
    r = requests.get(
        DEFAULT_BOT_LOGS_ENDPOINT,
        params={
            'uid': auth.uid,
            'key': auth.key,
            'bot_uid': bot_uid,
            'errors': True if errors else None
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
        timestamp = datetime.fromtimestamp(log['timestamp'] / 1000).isoformat(timespec='seconds')
        severity = log['severity']
        is_error = severity == 'ERROR'
        _log = logger.error if is_error else logger.info
        _log(f"===== LOG AT {timestamp} (SEVERITY: {severity}) =====")
        print(log['log'], file=sys.stderr if is_error else sys.stdout, flush=True)
        _log("===== END LOG =====")