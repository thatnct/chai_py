import imghdr
import inspect
import json
import os
import pprint
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Type, AnyStr
from zipfile import ZipFile, ZIP_DEFLATED

import requests

from .chai_bot import ChaiBot


@dataclass
class Metadata:
    name: str
    image_url: str
    color: str
    developer_uid: str
    description: str
    input_class: Type[ChaiBot]


def package(metadata: Metadata):
    print("Running verification checks on metadata.")
    assert isinstance(metadata.name, str)
    assert len(metadata.name) >= 3, "Bot name has to be at least 3 characters"

    try:
        verify_image_url(metadata.image_url)
    except Exception:
        raise ValueError(f"Could not verify image url ({metadata.image_url})")

    assert isinstance(metadata.color, str)
    assert re.search(r"^(?:[0-9a-fA-F]{3}){1,2}$", metadata.color), \
        "Color has to be provided as the alphanumeric part of the hex code (e.g. ffffff)"

    bot_file = Path(inspect.getfile(metadata.input_class))

    metadata_dict = {
        'name': metadata.name,
        'imageUrl': metadata.image_url,
        'color': metadata.color,
        'developerUid': metadata.developer_uid,
        'description': metadata.description,
        'inputFile': bot_file.stem,
        'input_class': metadata.input_class.__name__,
    }
    print("Prepared metadata:")
    pprint.pprint(metadata_dict)

    print("Preparing temporary directory...")
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy files in bot directory
        def ignore(src, names):
            # Do not store pycache folder.
            if '__pycache__' in names:
                return ['__pycache__']
            return []
        shutil.copytree(bot_file.parent, temp_dir, dirs_exist_ok=True, ignore=ignore)
        # Write metadata.json
        with (Path(temp_dir) / "metadata.json").open("w") as f:
            json.dump(metadata_dict, f)

        # Create zip
        zip_path = bot_file.parent / "package.zip"
        with zip_path.open("wb") as f:
            zipfile_from_folder(temp_dir, f)
        print(f"Created zip package at {zip_path}.")


def verify_image_url(url: str):
    """Verifies that the provided url resolves to an image.

    Performs a GET request on the given url and performs a trivial (non-conclusive) check
    that the image type can be inferred from the received bytes.

    :param url:
    :return:
    """
    r = requests.get(url)
    try:
        imghdr.what(None, h=r.content)
    except Exception:
        raise ValueError(
            f"Could not verify image type from bytes "
            f"(response content-type of {r.headers.get('content-type')})"
        )


def zipfile_from_folder(folder: AnyStr, file):
    # Adapted from https://stackoverflow.com/a/17080988
    with ZipFile(file, "w", compression=ZIP_DEFLATED) as zip_archive:
        for root, dirs, files in os.walk(folder):
            # add directory (needed for empty dirs)
            zip_archive.write(root, os.path.relpath(root, folder))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename):  # regular files only
                    arcname = os.path.join(os.path.relpath(root, folder), file)
                    zip_archive.write(filename, arcname)
