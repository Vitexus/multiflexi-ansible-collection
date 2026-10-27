import importlib.util
import json
import pathlib
from unittest import mock

import pytest

spec = importlib.util.spec_from_file_location(
    "multiflexi_cli_utils",
    pathlib.Path(__file__).parents[2] / "plugins/module_utils/multiflexi_cli.py",
)
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class Exit(Exception):
    def __init__(self, **kw):
        self.kw = kw


class Fail(Exit):
    pass


def make_module(**params):
    m = mock.Mock()
    m._verbosity = 0
    m.params = dict(multiflexi_cli_path="multiflexi-cli", **params)
    m.exit_json.side_effect = lambda **kw: (_ for _ in ()).throw(Exit(**kw))
    m.fail_json.side_effect = lambda **kw: (_ for _ in ()).throw(Fail(**kw))
    return m


def proc(stdout="", returncode=0, stderr=""):
    return mock.Mock(stdout=stdout, returncode=returncode, stderr=stderr)


def run(module, **kw):
    with pytest.raises(Exit) as exc:
        cli.run_info(module, **kw)
    return exc.value


def test_list_passes_filters_and_paging():
    m = make_module(status="failed", limit=5, offset=None, order="D", fields=["id", "status"])
    with mock.patch.object(cli.subprocess, "run", return_value=proc(json.dumps([{"id": 9}]))) as sp:
        out = run(m, singular="job", plural="jobs", list_command="job:list", get_command="job:get",
                  selectors={"id": "--id"}, filters={"status": "--status"})
    assert sp.call_args[0][0] == ["multiflexi-cli", "job:list", "--status", "failed", "--limit", "5",
                                  "--order", "D", "--fields", "id,status", "--format", "json"]
    assert out.kw == dict(changed=False, count=1, jobs=[{"id": 9}])


def test_selector_fetches_single_record():
    m = make_module(uuid="u-1")
    with mock.patch.object(cli.subprocess, "run", return_value=proc(json.dumps({"id": 1}))) as sp:
        out = run(m, singular="application", plural="applications", list_command="application:list",
                  get_command="application:get", selectors={"id": "--id", "uuid": "--uuid"})
    assert sp.call_args[0][0] == ["multiflexi-cli", "application:get", "--uuid", "u-1", "--format", "json"]
    assert out.kw == dict(changed=False, found=True, application={"id": 1})


def test_not_found_is_null_even_with_nonzero_rc():
    m = make_module(id=7)
    with mock.patch.object(cli.subprocess, "run", return_value=proc(json.dumps({"status": "not found"}), returncode=1)):
        out = run(m, singular="job", plural="jobs", list_command="job:list", get_command="job:get", selectors={"id": "--id"})
    assert out.kw == dict(changed=False, found=False, job=None)


def test_error_status_fails():
    m = make_module()
    with mock.patch.object(cli.subprocess, "run", return_value=proc(json.dumps({"status": "error", "message": "boom"}), returncode=2)):
        with pytest.raises(Fail):
            cli.run_info(m, singular="user", plural="users", list_command="user:list")


def test_invalid_json_with_failure_fails():
    m = make_module()
    with mock.patch.object(cli.subprocess, "run", return_value=proc("not json", returncode=3, stderr="bad")):
        with pytest.raises(Fail):
            cli.run_info(m, singular="user", plural="users", list_command="user:list")


def test_wrapped_list_response_is_unwrapped():
    m = make_module()
    with mock.patch.object(cli.subprocess, "run", return_value=proc(json.dumps({"items": [{"id": 1}, {"id": 2}]}))):
        out = run(m, singular="user", plural="users", list_command="user:list")
    assert out.kw["count"] == 2
