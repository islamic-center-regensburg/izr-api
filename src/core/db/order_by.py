from pydantic import BaseModel


class OrderBy(BaseModel):
    attribute: str
    descending: bool = True


class OrderByAdapter:
    @classmethod
    def from_sort_strings(cls, sort_strings: list[str]) -> list[OrderBy]:
        return [
            OrderBy(
                attribute=sort_string.strip("-"), descending=sort_string.startswith("-")
            )
            for sort_string in sort_strings
        ]
