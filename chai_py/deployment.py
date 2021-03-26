import time
from pathlib import Path
from typing import AnyStr, Optional

import requests
import segno
from halo import Halo
from typing_extensions import TypedDict

from .defaults import DEFAULT_BOT_STATUS_ENDPOINT, DEFAULT_SIGNED_URL_CREATOR, GUEST_KEY, GUEST_UID


def upload_and_deploy(package: AnyStr, uid: str = GUEST_UID, key: str = GUEST_KEY, bot_uid: str = None) -> str:
    """Uploads the given archive, triggering deployment of the chatbot.

    :param package: Path to the packaged chatbot zip.
    :param uid: Developer Unique Identifier. Defaults to a guest UID.
    :param key: Developer key. Defaults to a valid key for the guest UID.
    :return bot_uid: Used to modify an existing bot: the UID of the previously-deployed bot.
    """
    package = Path(package)
    try:
        r = requests.get(
            f"{DEFAULT_SIGNED_URL_CREATOR}?uid={uid}&key={key}",
            params={'uid': uid, 'key': key, 'bot_uid': bot_uid}
        )
        try:
            r.raise_for_status()
        except Exception as e:
            raise RuntimeError(r.json())
    except Exception:
        raise RuntimeError("Failed to retrieve signed URL.")

    url = r.text
    if bot_uid is None:
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
    completed_processes = []

    MAXIMUM_ERROR_RETRIES = 10
    error_retries = 0

    spinner = Halo(text="Polling for progress...")
    spinner.start()

    time.sleep(5)  # Initial wait to avoid bot status error.

    while True:
        try:
            status = get_bot_status(bot_uid)
        except Exception as e:
            spinner.warn(f"Error getting bot status (uid: {bot_uid}): {e}")
            error_retries += 1
            if error_retries > MAXIMUM_ERROR_RETRIES:
                spinner.fail()
                print(f"Hit retry-on-error limit ({MAXIMUM_ERROR_RETRIES}).")
                break
            continue
        status_str = status['status']
        if status_str not in BOT_DEPLOYMENT_PROCESS:
            raise ValueError(f"Unknown status: {status_str}.")
        new_current_deployment_process = BOT_DEPLOYMENT_PROCESS.index(status_str)
        if new_current_deployment_process != current_deployment_process:
            # Completed new step(s)
            for step in BOT_DEPLOYMENT_PROCESS[:new_current_deployment_process + 1]:
                if step in completed_processes:
                    continue
                spinner.succeed(step)
                completed_processes.append(step)
            current_deployment_process = new_current_deployment_process
            if current_deployment_process + 1 < len(BOT_DEPLOYMENT_PROCESS):
                # If next step exists, set spinner to next step
                spinner.start(
                    f"Waiting for next step: {BOT_DEPLOYMENT_PROCESS[current_deployment_process + 1]}"
                )
            else:
                # Next step does not exist; wait for final deployment confirmation
                spinner.start("Waiting for active_deployment confirmation...")
        if 'activeDeployment' in status:
            new_active_deployment = status['activeDeployment']
            if active_deployment is None or new_active_deployment['timestamp'] != active_deployment['timestamp']:
                spinner.succeed("active_deployment")
                print(f"New active deployment: {new_active_deployment}")
                active_deployment = new_active_deployment
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
    r = requests.get(DEFAULT_BOT_STATUS_ENDPOINT, params={'bot_uid': bot_uid})
    r.raise_for_status()
    return r.json()


def advertise_deployed_bot(bot_uid: str) -> str:
    """Displays the url, a QR code, along with additional guidance.

    :param bot_uid:
    :return: The url.
    """
    url = f"chai://chai.ml/{bot_uid}"
    qr_code = segno.make_qr(url)
    qr_code.terminal()

    print("Scan the QR code with your phone to start a chat in the app!")
    print(f"Or check it out at {url}")

    while True:
        print("\nEnter one of the following keys to perform additional actions:")
        print(" [s] Save this QR code to an image file.")
        print(" [o] Open QR code in external viewer (if your terminal does not display it correctly).")

        key = input()
        if key == "s":
            path = input("Save QR code to: (Press [Enter] for default: 'qr.png') ")
            if len(path) == 0:
                path = "qr.png"
            qr_code.save(path, scale=10)
            print(f"Saved QR code to {path}.")
        elif key == "o":
            qr_code.show(scale=10)
        else:
            break

    return url
