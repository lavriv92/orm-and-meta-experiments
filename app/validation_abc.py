from typing import Optional

import rich

from orm import Model, validator, create_database, relation, RelationTypes

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
        if len(value) < 3:
            raise ValueError("Value length shold be longest then 6")

    @validator("age")
    def validate_min_age(self, value: int, *args, **kwargs):
        if value < 18:
            raise ValueError("Age must bet at least 18")


@relation("User", relation_type=RelationTypes.ONE_TO_MANY)
class Post(Model):
    title: str
    content: str

    def __str__(self):
        return f"Post(id={self.id}, title={self.title!r}, content={self.content!r})"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    db = create_database("sqlite3://my-database.sqlite3")

    with db.connection() as conn:
        # user = User(name="Ivan", age=18)

        # conn.add(user)
        # conn.commit()

        post = Post(title="test post", content="post content", user_id=1)

        post.user = "Test"

        print(post.user)

        # print("post.user", post.user)

        # conn.add(post)
        # conn.commit()

        # user = conn.get(User, 1)

        # posts = conn.select(Post)
        # posts_json = [p for p in posts]
        # print("posts: ", posts_json)
