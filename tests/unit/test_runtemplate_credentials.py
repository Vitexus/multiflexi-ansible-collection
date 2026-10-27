import importlib.util
import json
import pathlib
import sys
from unittest import mock

import pytest

spec = importlib.util.spec_from_file_location(
    "runtemplate_module",
    pathlib.Path(__file__).parents[2] / "plugins/modules/runtemplate.py",
)
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)


class FailJson(Exception):
    pass


def make_module(**params):
    m = mock.Mock()
    m.params = params
    m.fail_json.side_effect = lambda **kw: (_ for _ in ()).throw(FailJson(kw))
    return m


def test_auto_passes_requirements_and_reports_change():
    m = make_module(credential_requirements=["AbraFlexi"])
    with mock.patch.object(rt, "run_cli", return_value={"status": "ok", "changed": True}) as cli:
        assert rt.assign_credentials(m, 5) is True
    cli.assert_called_once_with(
        m, ["run-template:assign-credential", "--id", "5", "--auto", "--requirement", "AbraFlexi"]
    )


def test_unchanged_is_idempotent():
    m = make_module()
    with mock.patch.object(rt, "run_cli", return_value={"status": "ok", "changed": False}):
        assert rt.assign_credentials(m, 5) is False


def test_error_report_fails_task():
    m = make_module()
    with mock.patch.object(rt, "run_cli", return_value={"status": "error", "requirements": {"AbraFlexi": {"status": "ambiguous"}}}):
        with pytest.raises(FailJson):
            rt.assign_credentials(m, 5)


def test_want_credentials():
    assert rt.want_credentials(make_module(auto_credentials=True))
    assert rt.want_credentials(make_module(auto_credentials=False, credential_requirements=["X"]))
    assert not rt.want_credentials(make_module(auto_credentials=False, credential_requirements=None))
