#FastAPI is a python class that provides all the functionality for your API.
from fastapi import FastAPI, Query
#importing enum, Enum stands for enumeration. It is a way of creating a pre defined values. It deprives the user to enter random values and only limit the choice to the few predefined options.
from enum import Enum
#importing basemodel from pydantic
from pydantic import BaseModel
from typing import Optional, Annotated

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
async def read_items(name: Annotated[Optional[str], Query(max_length=5)] = None):#here, name is optional, so we use Optional[str]. This means the type of name can be str or None. The = None means its default value is None (so the client can omit it). The Query(max_length=5) restricts the query parameter to have at most 5 characters if provided.
    return{"Name": name}
