"""Query synthetic business records in a short-lived in-memory SQLite database."""
from contextlib import closing
import sqlite3


def integer(value, name, minimum=0, maximum=1000000):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError("{} must be an integer from {} to {}".format(name, minimum, maximum))
    return value


def query_directory(data):
    if not isinstance(data, dict) or not isinstance(data.get("businesses"), list) or len(data["businesses"]) > 1000:
        raise ValueError("Supply an object with at most 1000 businesses")
    after = integer(data.get("after_id", 0), "after_id")
    limit = integer(data.get("limit", 10), "limit", 1, 50)
    search, city, category = (data.get(key, "") for key in ("search", "city", "category"))
    if any(not isinstance(value, str) or len(value) > 100 for value in (search, city, category)):
        raise ValueError("Search and filters must be text of at most 100 characters")
    rows, seen = [], set()
    for item in data["businesses"]:
        if not isinstance(item, dict):
            raise ValueError("Business records must be objects")
        key = integer(item.get("id"), "id", 1)
        if key in seen:
            raise ValueError("Business IDs must be unique")
        seen.add(key)
        values = [item.get(field) for field in ("name", "city", "category")]
        if any(not isinstance(value, str) or not 1 <= len(value.strip()) <= 100 for value in values):
            raise ValueError("Business name, city, and category need 1–100 characters")
        rows.append((key, *(value.strip() for value in values)))
    with closing(sqlite3.connect(":memory:")) as db:
        db.row_factory = sqlite3.Row
        db.execute("CREATE TABLE businesses(id INTEGER PRIMARY KEY, name TEXT, city TEXT, category TEXT)")
        db.executemany("INSERT INTO businesses VALUES(?,?,?,?)", rows)
        clauses, params = ["id > ?"], [after]
        if search:
            clauses.append("instr(lower(name), lower(?)) > 0")
            params.append(search)
        for field, value in (("city", city), ("category", category)):
            if value:
                clauses.append("lower(" + field + ") = lower(?)")
                params.append(value.strip())
        sql = "SELECT * FROM businesses WHERE " + " AND ".join(clauses) + " ORDER BY id LIMIT ?"
        found = [dict(row) for row in db.execute(sql, (*params, limit + 1))]
    items = found[:limit]
    return {"items": items, "next_cursor": items[-1]["id"] if len(found) > limit else None}
