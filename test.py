#FastAPI is a python class that provides all the functionality for your API.
from fastapi import FastAPI, Query, Path
#importing enum, Enum stands for enumeration. It is a way of creating a pre defined values. It deprives the user to enter random values and only limit the choice to the few predefined options.
from enum import Enum
#importing basemodel from pydantic
from pydantic import BaseModel, AfterValidator, Field
from typing import Optional, Annotated, Literal

app = FastAPI()
#Creating an instances called "app" of the class FastAPI
#app will be the main point of interaction to create all your APIs.

@app.get("/")
#Creating a path. Path will start from the first /.
#Here get is one of the HTTP methods. It is also known as operations. Other mainly used HTTP methods are put, post and delete.
#get is used to retrive the data.
#Here, the @app.get("/") tells FastAPi that the function right below is in charge of handling requests that go in the path / using a get operation. 
def root():
#defining a function
    return{"message": "hello world"}
    #returning a message that simply means hello world




#Path and Query Parameters
#Path Parameters

#Path parameters are declared using curly braces in the route path and are automatically converted to the specified type. 
@app.get("/items/{item_id}")
def view_item(item_id: int):
    return{"item_id": item_id}


#Getting the Concept of the Enum
class Genre(str, Enum):
    action = "action"
    comedy = "comedy"
    drama = "drama"
#Here, the left side is the member of the enumeration and right side is the actual value.

#Now, here I have used the path parameter.
@app.get("/movies/genre/{genre_name}")
def get_movies_by_genre(genre_name: Genre):
    return {"selected_genre": genre_name}




#Query Parameters
#Query parameters typically comes after the question mark. They are generally used for sorting, filtering etc.
@app.get("/query_param/")
def search_movies(genre: str = None, year: int = None):
    return{"genre": genre, "year": year}

#Here, we have used the query parameter to get a filter of genre and year. 



#Applying query parameter and path parameter at the same time
#get movies by genre(path parameter) and year(query parameter)
class Genre (str, Enum):
    comedy = "comedy"
    action = "action"
    drama = "drama"
#path parameter
@app.get("/movies_by_genre/{genre_name}")#This is an actual path parameter.
def get_movies_by_genre(genre_name: Genre, year:int = None):#This is a query parameter.
    if year:
        return {
            "message": f"fetching {genre_name} released in {year}"
        }

    return{
            "message": f"fetching all {genre_name} movies"
        }




#Request Body
#Request Body are declared using Pydantic Models. These models provide data validation.
#First, you need to import BaseModel from pydantic.
class Item(BaseModel):
    name: str
    price: Optional[float]#price is optional.
    tax: Optional[float]#tax is optional.

items = []
#As the request body is generally used in the POST and PUT or PATCH, here post is used.
@app.post("/add_items/")
def create_item(item: Item):
    items.append(item)
    return item


#Now, let us view the data that we just inserted
@app.get("/view_items/")
def view_items():
    return{"item": items}




# String Validations: String validation means checking that a string value follows certain rules before you accept it. For example: Minimum length (eg: 3 characters) , Maximum length (eg: 10 characters)
#Why we do it?
#a. To prevent bad data(eg: empty name)
#b. To protect your app from error


#let us see some demonstration here:
#we need to import 2 things before doing string validation.
#a. Qurey from fastapi
#b. Annotated from typing


@app.get("/name/")
async def read_items(name: Annotated[Optional[str], Query(max_length=5, min_length=1)] = None):
    # here, name is optional, so we use Optional[str]. This means the type of name can be str or None. 
    # The = None means its default value is None (so the client can omit it). 
    # The Query(max_length=5) restricts the query parameter to have at most 5 characters if provided.
    return {"Name": name}


#you can also pre-define the value of name without defining it none.
@app.get("/name/")
async def read_name(name: Annotated[str, Query(max_length = 5)] = "jojo"):
    return{"name": name}

#here, = "jojo" means i have a predefined value for name which is jojo.



#Custom Validation
#Sometimes built in validators are not enough. You want to add your own login to check the data. 


def check_name(value: str):
    if value.lower() == "foo":
        raise ValueError('name cannot be "foo"')
    return value

@app.get("/items/")
async def read_items(
    name: Annotated[str, AfterValidator(check_name)]
):
    return {"name": name}
#Explanation
# name is a query parameter.
# AfterValidator(check_name) applies your custom validation function after parsing.
# If name is "foo" (case-insensitive), it raises a validation error.
# Otherwise, it returns the name.






#Path Parameter and Numeric Validation
#Need to import path from fastapi and Annotated from typing
@app.get("/read_items/{item_id}")
def read_items(
    item_id: Annotated[int, Path(title="The id of the item to get")], 
    q: Annotated[Optional[str], Query(Alias="item query")] = None
):
    results = {"item_id": item_id}
    if q:
        results.update({"q":q})
    return results


#here, our function [read_items] takes 2 parameters: 
#1. item_id: comes from the path parameter
#2. q: from query string

# In line 163, int is the data type of the item_id, path here add a title or a metadata and annotated let us combine the typehints plus validation info.
#Now as for the Alias, Alias basically lets how rename how the user writes the parameter.
# Here, Query(Alias="item query") We want the query parameter to be called item query in the URL, not just q.
#In Python, you can’t have spaces in variable names (q is the Python name).
#In the URL, you can use spaces — but in URLs, spaces are written as %20.






#Query Parameter Model
#Normally, Query parameters are simple such as: ?q=apple&skip=0&limit=10        [q, skip and limit]
#But What if there are numerous query parameters? In this case, we make a basemodel of Query parameter and store all the query parameters there for reusability.
class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(100, gt=0, le=100) #here ,the limit should be of integer with the value greater than 0 or smaller than or equal to 100. If not provided, default value becomes 100.
    offset: int = Field(0, ge=0)#here, it says the value should start from 0. if not provided, default value becomes 0.
    order_by: Literal["created_at", "updated_at"] = "created_at" #here, must be either, created_at or updated_at. But the default value is created_at.
    tags: list[str] = []#It can have multiple tags. Such as tags=tech&tags=ai.


@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
# FastAPI sees that your function wants a filter_query.
# You told FastAPI:

# filter_query should be built using the FilterParams Pydantic model
# The Query() part says “Read it from query parameters, not the request body.”

# FastAPI does:
# Looks at the URL.
# Finds limit, offset, order_by, tags.
# Makes a FilterParams object using those values.
# Gives that object to your filter_query parameter.



#In some special cases, you want to restrict the query parameters that you want to recieve. You can use pydantic model to forbid any extra fields.
#see in line 193.





#Body - Multiple Parameters
#Here is a advance use of the body request declarations
#Here, I have used two basemodels i.e. Item and User. Item contains the info about the items and user contains the info about the user's details.
class Item(BaseModel):
    name: str
    description: Optional[str]
    price: Optional[int]
    tax: Optional[int]
    #here, left side contains the varaibles and right side contains the data type.

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    
@app.get("/items{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": {item_id}, "item": {item}, "user": {user}}
    return results
