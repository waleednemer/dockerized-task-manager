import datetime

import app as app_module

clean = app_module.clean


def test_title_required():
    data, err = clean({"title": "   "})
    assert data is None and err == "العنوان مطلوب"


def test_title_trimmed_and_limited():
    data, _ = clean({"title": "  " + "x" * 300 + "  "})
    assert len(data["title"]) == 200


def test_invalid_status_rejected():
    _, err = clean({"title": "a", "status": "finished"})
    assert err == "حالة غير صالحة"


def test_invalid_priority_rejected():
    _, err = clean({"title": "a", "priority": "urgent"})
    assert err == "أولوية غير صالحة"


def test_invalid_date_rejected():
    _, err = clean({"title": "a", "due_date": "25-11-2026"})
    assert err == "تاريخ غير صالح"


def test_valid_date_parsed_and_empty_date_is_none():
    data, _ = clean({"title": "a", "due_date": "2026-11-25"})
    assert data["due_date"] == datetime.date(2026, 11, 25)
    data, _ = clean({"title": "a", "due_date": ""})
    assert data["due_date"] is None


def test_partial_update_does_not_require_title():
    data, err = clean({"status": "done"}, partial=True)
    assert err is None and data == {"status": "done"}
