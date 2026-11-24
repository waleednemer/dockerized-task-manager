import os
import pathlib
import sys
from contextlib import closing

import psycopg2
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import app as app_module  # noqa: E402

INIT_SQL = pathlib.Path(__file__).resolve().parents[2] / "database" / "init.sql"


@pytest.fixture(scope="session")
def _schema():
    try:
        conn = app_module.connect()
    except psycopg2.OperationalError as e:
        # في CI نريد الفشل لا التخطي، حتى لا ينجح البناء بدون اختبار فعلي
        if os.getenv("CI"):
            pytest.fail(f"PostgreSQL not available in CI: {e}")
        pytest.skip(f"PostgreSQL not available: {e}")
    with conn, conn.cursor() as cur:
        cur.execute(INIT_SQL.read_text())
    conn.close()


@pytest.fixture
def client(_schema):
    with closing(app_module.connect()) as conn, conn, conn.cursor() as cur:
        cur.execute("TRUNCATE tasks RESTART IDENTITY")
    return app_module.app.test_client()
