import pytest
from tina4_python.MiddleWare import MiddleWare

# Positive test middleware class
class SampleMiddleware:
    def before_validate(self, req, res):
        req["stage"] = "before"
        return req, res

    def after_process(self, req, res):
        res["stage"] = "after"
        return req, res

    def transform(self, req, res):
        req["custom"] = "transform"
        return req, res


# Negative test: empty middleware
class EmptyMiddleware:
    pass

# Negative test: edge case classification
class EdgeCaseMiddleware:
    def beforenoon(self, req, res):
        req["edge"] = "not a before"
        return req, res


@pytest.fixture
def blank_request_response():
    return {}, {}

# MIDDLEWARE-001 to 003
def test_method_classification():
    mw = MiddleWare(SampleMiddleware())
    assert "before_validate" in mw.before_methods
    assert "after_process" in mw.after_methods
    assert "transform" in mw.any_methods
    assert mw.middleware_class is not None

# MIDDLEWARE-004
def test_call_before_methods(blank_request_response):
    mw = MiddleWare(SampleMiddleware())
    req, res = mw.call_before_methods(*blank_request_response)
    assert req["stage"] == "before"

# MIDDLEWARE-005
def test_call_after_methods(blank_request_response):
    mw = MiddleWare(SampleMiddleware())
    req, res = mw.call_after_methods(*blank_request_response)
    assert res["stage"] == "after"

# MIDDLEWARE-006
def test_call_any_methods(blank_request_response):
    mw = MiddleWare(SampleMiddleware())
    req, res = mw.call_any_methods(*blank_request_response)
    assert req["custom"] == "transform"

# MIDDLEWARE-007
def test_call_direct_method(blank_request_response):
    mw = MiddleWare(SampleMiddleware())
    req, res = mw.call_direct_method(*blank_request_response, method_name="transform")
    assert req["custom"] == "transform"

# MIDDLEWARE-008
def test_empty_middleware_classification():
    mw = MiddleWare(EmptyMiddleware())
    assert mw.before_methods == []
    assert mw.after_methods == []
    assert mw.any_methods == []

# MIDDLEWARE-009
def test_invalid_direct_method_raises(blank_request_response):
    mw = MiddleWare(SampleMiddleware())
    with pytest.raises(AttributeError):
        mw.call_direct_method(*blank_request_response, method_name="non_existent")

# MIDDLEWARE-010
def test_edge_case_method_classification():
    mw = MiddleWare(EdgeCaseMiddleware())
    assert "beforenoon" in mw.any_methods  # Should not be mistaken for "before"
