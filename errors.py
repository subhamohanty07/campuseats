"""Small JSON error helper used by the CampusEats service."""


def problem(status, title, detail, type_="about:blank"):
    return {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail,
    }
