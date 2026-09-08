def problem(status, title, detail, problem_type=None):
    return {
        "type": problem_type
        or (
            "https://api.campuseats.example.com/problems/"
            f"{title.lower().replace(' ', '-')}"
        ),
        "title": title,
        "status": status,
        "detail": detail,
    }


class OrderError(Exception):

    def __init__(self, status, title, detail):

        self.status = status
        self.title = title
        self.detail = detail

        super().__init__(detail)