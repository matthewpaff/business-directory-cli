"""Original listing-query cases, constructed without using the implementation."""


def make_case(index):
    key = index * 10 + 1
    a = {"id": key, "name": "Sample Cafe {}%".format(index), "city": "Town", "category": "cafe"}
    b = {"id": key + 1, "name": "Book Shop {}".format(index), "city": "Town", "category": "books"}
    c = {"id": key + 2, "name": "Remote Cafe {}".format(index), "city": "Elsewhere", "category": "cafe"}
    data = {"businesses": [c, b, a]}
    kind = index % 10
    if kind == 0:
        data["businesses"] = [a, dict(a)]
        description = "reject duplicate business IDs"
    elif kind == 1:
        data["businesses"] = [{"id": key, "city": "Town", "category": "cafe"}]
        description = "reject listings without a name"
    elif kind == 2:
        data["limit"] = 0
        description = "reject zero-sized pages"
    elif kind == 3:
        data["after_id"] = -1
        description = "reject negative pagination cursors"
    elif kind == 4:
        data["businesses"] = [{**a, "id": True}]
        description = "reject booleans as listing IDs"
    elif kind == 5:
        data["limit"] = 1
        expected = {"items": [a], "next_cursor": key}
        description = "return the first keyset page in ascending ID order"
    elif kind == 6:
        data["city"] = "town"
        expected = {"items": [a, b], "next_cursor": None}
        description = "match city filters without ASCII case sensitivity"
    elif kind == 7:
        data.update({"category": "cafe", "after_id": key})
        expected = {"items": [c], "next_cursor": None}
        description = "combine category filtering with a keyset cursor"
    elif kind == 8:
        data["search"] = "%"
        expected = {"items": [a], "next_cursor": None}
        description = "treat percent signs as literal search text"
    else:
        data["search"] = "' OR 1=1 --"
        expected = {"items": [], "next_cursor": None}
        description = "treat SQL-like search text as a parameter"
    result = {"id": "directory-{:04d}".format(index), "description": description, "input": data}
    result.update({"expected_error": True} if kind < 5 else {"expected": expected})
    return result
