from pathlib import Path
from typing import AnyStr

import requests

from .defaults import DEFAULT_SIGNED_URL_CREATOR, DEFAULT_UID


def upload_and_deploy(package: AnyStr, uid: str = DEFAULT_UID):
    """Uploads the given archive, triggering deployment of the chatbot.

    :param package: Path to the packaged chatbot zip.
    :param uid:
    :return:
    """
    package = Path(package)

    try:
        r = requests.get(
            f"{DEFAULT_SIGNED_URL_CREATOR}?uid={uid}"
        )
        r.raise_for_status()
    except Exception:
        raise RuntimeError("Failed to retrieve signed URL.")

    url = r.text
    with package.open("rb") as f:
        r = requests.put(url, data=f, headers={'content-type': 'application/zip'})
        r.raise_for_status()
    print(f"Successfully uploaded {package}.")
