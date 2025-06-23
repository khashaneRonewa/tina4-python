import pytest
from datetime import datetime, date
from decimal import Decimal
from tina4_python.DatabaseResult import DatabaseResult


# DBR-001
def test_init_with_records_and_columns():
    result = DatabaseResult(_records=[{"id": 1}], _columns=["id"])
    assert result.records == [{"id": 1}]
    assert result.columns == ["id"]
    assert result.count == 1


# DBR-002
def test_to_array_with_simple_record():
    result = DatabaseResult(_records=[{"id": 1}], _columns=["id"])
    array_output = result.to_array()
    assert array_output == [{"id": 1}]


# DBR-003
def test_to_json_conversion():
    result = DatabaseResult(_records=[{"id": 1}], _columns=["id"])
    json_output = result.to_json()
    assert json_output == '[{"id": 1}]'


# DBR-004
def test_to_paginate_with_data():
    result = DatabaseResult(_records=[{"id": 1}], _columns=["id"], count=1, limit=10, skip=0)
    pagination = result.to_paginate()
    assert pagination["recordsTotal"] == 1
    assert pagination["fields"] == ["id"]
    assert pagination["data"] == [{"id": 1}]


# DBR-005
def test_to_array_handles_decimal():
    result = DatabaseResult(_records=[{"price": Decimal("10.5")}], _columns=["price"])
    assert result.to_array() == [{"price": 10.5}]


# DBR-006
def test_to_array_handles_datetime():
    result = DatabaseResult(_records=[{"date": datetime(2023, 1, 1)}], _columns=["date"])
    assert result.to_array() == [{"date": "2023-01-01T00:00:00"}]


# DBR-006 (continued for date)
def test_to_array_handles_date():
    result = DatabaseResult(_records=[{"date": date(2023, 1, 1)}], _columns=["date"])
    assert result.to_array() == [{"date": "2023-01-01"}]


# DBR-007
def test_to_array_handles_bytes():
    result = DatabaseResult(_records=[{"img": b"abc"}], _columns=["img"])
    output = result.to_array()
    assert output[0]["img"] == "YWJj"  # base64 of b"abc"


# DBR-008
def test_to_array_with_filter_function():
    result = DatabaseResult(_records=[{"id": 1}], _columns=["id"])
    filtered = result.to_array(_filter=lambda x: {"new_id": x["id"]})
    assert filtered == [{"new_id": 1}]


# DBR-009
def test_error_handling_in_to_array():
    result = DatabaseResult(_error="DB connection failed")
    output = result.to_array()
    assert output == {"error": "DB connection failed"}


# DBR-010
def test_empty_initialization():
    result = DatabaseResult()
    assert result.records == []
    assert result.count == 0


# DBR-011
def test_out_of_bounds_index_returns_empty():
    result = DatabaseResult(_records=[{"id": 1}])
    out = result[1]
    assert out == {}


# DBR-012
def test_invalid_filter_function_raises():
    result = DatabaseResult(_records=[{"id": 1}], _columns=["id"])
    with pytest.raises(TypeError):
        result.to_array(_filter="not_a_function")
