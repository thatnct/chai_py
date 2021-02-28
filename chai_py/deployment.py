from pathlib import Path
from typing import AnyStr

import requests

from .defaults import DEFAULT_SIGNED_URL_CREATOR, GUEST_UID, GUEST_KEY


def upload_and_deploy(package: AnyStr, uid: str = GUEST_UID, key: str = GUEST_KEY):
    """Uploads the given archive, triggering deployment of the chatbot.

    :param package: Path to the packaged chatbot zip.
    :param uid: Developer Unique Identifier. Defaults to a guest UID.
    :param key: Developer key. Defaults to a valid key for the guest UID.
    :return:
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
