import os
import types
import pytest
from datetime import datetime, date
from unittest.mock import MagicMock

import tina4_python
from tina4_python.Template import Template
from tina4_python.Session import Session


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setenv("TINA4_DEBUG_LEVEL", "ALL")
    if hasattr(Template, "twig"):
        delattr(Template, "twig")
    yield


def test_init_twig_creates_environment(tmp_path):
    twig = Template.init_twig(str(tmp_path))
    assert twig is Template.twig
    twig2 = Template.init_twig(str(tmp_path))
    assert twig2 is twig
    assert "RANDOM" in twig.globals
    assert "formToken" in twig.globals


def test_production_dump_and_dump():
    assert Template.production_dump("x") == ""
    result = Template.dump({"a": 1})
    assert result.startswith("<pre>")
    assert '"a": 1' in result
    d = date(2020, 1, 1)
    assert "2020-01-01" in Template.dump({"d": d})
    dt = datetime(2020, 1, 1, 12, 0)
    assert "2020-01-01T12:00:00" in Template.dump({"dt": dt})
    # Use a real Session subclass so isinstance works
    class DummySession(Session):
        def __init__(self):
            self.session_values = {"x": 1}
    assert "x" in Template.dump({"s": DummySession()})
    assert Template.dump(None) == ""


def test_get_form_token_and_input(monkeypatch):
    monkeypatch.setattr(tina4_python, "tina4_auth", MagicMock())
    tina4_python.tina4_auth.get_token.return_value = "TOKEN123"
    assert Template.get_form_token({"a": 1}) == "TOKEN123"
    html = Template.get_form_token_input("form1")
    assert "TOKEN123" in html


def test_convert_special_types():
    d = {"a": datetime(2020, 1, 1, 12, 0), "b": [date(2020, 1, 1)]}
    out = Template.convert_special_types(d)
    assert out["a"] == "2020-01-01T12:00:00"
    assert out["b"][0] == "2020-01-01"
    assert Template.convert_special_types("x") == "x"


def test_render_twig_template_from_string(monkeypatch):
    fake_env = MagicMock()
    fake_env.get_template.side_effect = Exception("template not found")
    # Patch to actually use from_string in the try block
    def fake_get_template(name):
        raise Exception("no file")
    fake_env.get_template = fake_get_template
    fake_env.from_string.return_value.render.return_value = "rendered content"
    monkeypatch.setattr(Template, "init_twig", lambda path: fake_env)
    tina4_python.root_path = "root"
    tina4_python.tina4_current_request = {"req": "data"}
    # Here, we mimic the path where get_template returns falsy
    fake_env.get_template = lambda name: None
    out = Template.render_twig_template("string template", {"name": "test"})
    assert out == "rendered content"


def test_render_twig_template_error(monkeypatch):
    fake_env = MagicMock()
    fake_env.get_template.side_effect = Exception("boom")
    monkeypatch.setattr(Template, "init_twig", lambda path: fake_env)
    tina4_python.root_path = "root"
    tina4_python.tina4_current_request = {}
    out = Template.render_twig_template("anything", {})
    assert "boom" in out


def test_render_calls_render_twig_template(monkeypatch):
    monkeypatch.setattr(Template, "render_twig_template", lambda n, d=None: "OK")
    assert Template.render("name") == "OK"
