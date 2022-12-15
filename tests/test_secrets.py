"""Attempt to import secret data"""

import os

import yaml

from operationbot.models.config import Secret


def test_secret_import_yaml(datadir):
    """Read up a secret as yaml"""
    with open(datadir / "sample_secret.yaml") as secret_fd:
        secret_dict = yaml.safe_load(secret_fd)
    secret_obj = Secret.parse_obj(secret_dict)
    assert secret_obj.token == "super secret token", "Incorrect yaml secret parsing"


def test_secret_import_envvar(mocker):
    """Read the secrets from envvar"""
    ENV = {
        "OPBOT_VERSION": "1",
        "OPBOT_TOKEN": "super secret token",
        "OPBOT_COMMAND_CHAR": "!",
        "OPBOT_ADMINS": "[12345]",
        "OPBOT_ADMIN": "0",
        "OPBOT_DEBUG": "False",
        "OPBOT_SIGNOFF_NOTIFY_USER": "0",
        "OPBOT_PLATOON_SIZE": "1PLT",
        "OPBOT_WW2_MODS": "",
    }
    mocker.patch.dict(os.environ, ENV)
    secret_obj = Secret()
    assert secret_obj.token == "super secret token", "Incorrect envvar secret parsing"
