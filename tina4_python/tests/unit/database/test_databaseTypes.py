import pytest
import tina4_python.DatabaseTypes as dbt


# DBTYPES-001
def test_sqlite_constant():
    assert dbt.SQLITE == "sqlite3"


# DBTYPES-002
def test_firebird_constant():
    assert dbt.FIREBIRD == "firebird.driver"


# DBTYPES-003
def test_mysql_constant():
    assert dbt.MYSQL == "mysql.connector"


# DBTYPES-004
def test_postgres_constant():
    assert dbt.POSTGRES == "psycopg2"


# DBTYPES-005
def test_mssql_constant():
    assert dbt.MSSQL == "pymssql"


# DBTYPES-006
def test_firebird_install_string():
    assert dbt.FIREBIRD_INSTALL.startswith("pip install firebird-driver")


# DBTYPES-007
def test_mysql_install_string():
    assert dbt.MYSQL_INSTALL.startswith("pip install mysql-connector-python")


# DBTYPES-008
def test_postgres_install_string():
    assert dbt.POSTGRES_INSTALL.startswith("pip install psycopg2-binary")


# DBTYPES-009
def test_mssql_install_string():
    assert dbt.MSSQL_INSTALL.startswith("pip install pymssql")


# DBTYPES-010
def test_accessing_undefined_constant_raises():
    with pytest.raises(AttributeError):
        _ = getattr(dbt, "NON_EXISTENT_CONSTANT")
