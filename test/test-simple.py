from typing import List, Optional, Union, TypedDict, Any

class Status(str):
    "active",
    "inactive",

class Person(TypedDict):
    name: Required[str]
    age: Required[int]
    status: Required[Status]

class TestAgent(TypedDict):
    id: Required[str]
    person: Required[Person]