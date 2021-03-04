import time
from pathlib import Path
from typing import AnyStr, TypedDict, Optional

import requests

from .defaults import DEFAULT_SIGNED_URL_CREATOR, GUEST_UID, GUEST_KEY


def upload_and_deploy(package: AnyStr, uid: str = GUEST_UID, key: str = GUEST_KEY) -> str:
    """Uploads the given archive, triggering deployment of the chatbot.

    :param package: Path to the packaged chatbot zip.
    :param uid: Developer Unique Identifier. Defaults to a guest UID.
    :param key: Developer key. Defaults to a valid key for the guest UID.
    :return bot_uid: The UID of the deployed bot.
    """
    package = Path(package)

    try:
        r = requests.get(
            f"{DEFAULT_SIGNED_URL_CREATOR}?uid={uid}&key={key}"
        )
        r.raise_for_status()
    except Exception:
        raise RuntimeError("Failed to retrieve signed URL.")

    url = r.text
    bot_uid = parse_signed_url_for_bot_uid(url)
    print(f"Received bot UID: {bot_uid}")
    with package.open("rb") as f:
        r = requests.put(url, data=f, headers={'content-type': 'application/zip'})
        r.raise_for_status()
    print(f"Successfully uploaded {package}.")
    return bot_uid


def parse_signed_url_for_bot_uid(url: str):
    """Parses a bot UID from a signed URL.

    Assumes the signed URL follows the following scheme:
        [...]/{bot_uid}.zip?[...]

    :param url:
    :return:
    """
    endpoint = url.split("?", maxsplit=1)[0]
    file_name = endpoint.split("/")[-1]
    bot_uid = file_name.split(".")[0]
    return bot_uid


def wait_for_deployment(bot_uid: str, sleep: float = 3):
    """Waits for deployment of the bot to complete.

    :param bot_uid:
    :param sleep: Polling interval in seconds.
    :return:
    """
    MIN_SLEEP = 1
    sleep = max(MIN_SLEEP, sleep)

    BOT_DEPLOYMENT_PROCESS = [
        "signed_url_created",
        "processing_upload",
        "deploying",

        "initialized",
        # sent_message
        # (These two are repeatedly set as and when the function is restarted/invoked)
    ]
    current_deployment_process = -1  # Index for BOT_DEPLOYMENT_PROCESS
    active_deployment = None  # TODO: Poll for existing deployment to detect new vesion later.

    MAXIMUM_ERROR_RETRIES = 10
    error_retries = 0
    while True:
        try:
            status = get_bot_status(bot_uid)
            status_str = status['status']
            if status_str not in BOT_DEPLOYMENT_PROCESS:
                raise ValueError(f"Unknown status: {status_str}.")
            new_current_deployment_process = BOT_DEPLOYMENT_PROCESS.index(status_str)
            if new_current_deployment_process != current_deployment_process:
                print(f"{new_current_deployment_process} (from: {current_deployment_process})")
                current_deployment_process = new_current_deployment_process
            if 'activeDeployment' in status:
                new_active_deployment = status['activeDeployment']
                if active_deployment is None or new_active_deployment['timestamp'] != active_deployment['timestamp']:
                    print(f"New active deployment: {new_active_deployment}")
                    active_deployment = new_active_deployment
                    break
        except Exception as e:
            print(f"Error getting bot status (uid: {bot_uid}): {e}")
            error_retries += 1
            if error_retries > MAXIMUM_ERROR_RETRIES:
                print(f"Hit retry-on-error limit ({MAXIMUM_ERROR_RETRIES}).")
                break
        time.sleep(sleep)


class ActiveDeployment(TypedDict):
    timestamp: int
    version: int


class BotStatus(TypedDict):
    status: str
    timestamp: int
    activeDeployment: Optional[ActiveDeployment]


def get_bot_status(bot_uid: str) -> BotStatus:
    """Gets the status of the bot.

    :param bot_uid:
    :return:
    """
    r = requests.get(DEFAULT_SIGNED_URL_CREATOR, params={'bot_uid': bot_uid})
    r.raise_for_status()
    return r.json()
