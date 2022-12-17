"""Attempt to import secret data"""

import os

import pytest
import yaml
from pydantic import ValidationError

from operationbot.models.config import Secret

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


def test_secret_import_yaml(datadir):
    """Read up a secret as yaml"""
    with open(datadir / "sample_secret.yaml") as secret_fd:
        secret_dict = yaml.safe_load(secret_fd)
    secret_obj = Secret.parse_obj(secret_dict)
    assert secret_obj.token == ENV["OPBOT_TOKEN"], "Incorrect yaml secret parsing"


def test_secret_import_envvar(mocker):
    """Read the secrets from envvar"""
    mocker.patch.dict(os.environ, ENV)
    secret_obj = Secret()
    assert secret_obj.token == ENV["OPBOT_TOKEN"], "Incorrect envvar secret parsing"


def test_secret_import_badversion(mocker):
    """Showcase incorrect versions rejected"""
    mocker.patch.dict(os.environ, ENV)
    more_env = {"OPBOT_VERSION": "123"}
    mocker.patch.dict(os.environ, more_env)
    with pytest.raises(ValidationError):
        Secret()
