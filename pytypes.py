def get_full_name(firstname: str, lastname: str):
    fullname = firstname.title() + " " + lastname.title()
    return fullname

print(get_full_name("aashish", "rokka"))
# print(get_full_name(firstname="john", lastname="doe"))

def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this year old :" + str(age)
    return name_with_age

print(get_name_with_age("jojo", 21))

def types(item_a: int, item_b: float, item_c: bool, item_d: bytes, item_e: str):
    return (item_a, item_b, item_c, item_d, item_e)


import datetime
from typing import Optional
def say_hi(name:Optional[str] = None):
    if name is not None:
        print(f"Hello, {name}")
    else:
        print("Hello World")

say_hi(name = "jojo")


from typing import Union


def say_hi(name: Union[str, None] = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")

say_hi()

from typing import Optional
def say_hi(name: Optional[str] = None):
    print(f"Hello {name}")

say_hi()


#Pydantic model
from datetime import datetime
from typing import Union
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: Union[datetime, None] = None
    friends : list[int]=[]

external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}

user = User(**external_data)
print(user)