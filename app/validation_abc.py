from typing import Optional

import rich

from orm import Model, validator, create_database

print = rich.print


class User(Model):
    name: str
    age: Optional[int]

    def __str__(self):
        return f"User(id={self.id}, name={self.name!r}, age={self.age})"

    def __repr__(self) -> str:
        return self.__str__()

    @validator("name")
    def validate_name(self, value: str, *args, **kwargs):
        if len(value) < 6:
            raise ValueError("Value length shold be longest then 6")

    @validator("age")
    def validate_min_age(self, value: int, *args, **kwargs):
        if value < 18:
            raise ValueError("Age must bet at least 18")


if __name__ == "__main__":
    db = create_database("sqlite3://my-database.sqlite3")

    with db.connection() as conn:
        user = conn.get(User, 1)

        users = conn.select(User)

        users_json = [u.dict for u in users]

        print("users: ", users_json)

        print("user", user)

        # user = User(name="Example user", age=18)

        # user = conn.add(user)
        # conn.commit()

        # print("new user", user)

    # try:
    #     user = User(**{"name": "Test User", "age": 18})

    #     with create_database("sqlite3://my-database.sqlite3") as db:
    #         db.add(user)
    #         db.commit()

    #         # results = db.select(User)

    #         # print("r", results)

    #         # print("user", u.dict)
    # except ValidationError as e:
    #     print("errors:", e.json)
