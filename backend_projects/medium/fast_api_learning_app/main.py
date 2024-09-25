from typing import Annotated

from fastapi import FastAPI, Query, Body

app = FastAPI()


# basic get operation
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/path")
async def path():
    return {"message": "you called the /path endpoint"}


# let's add some arguments / parameters in the query itself
@app.get("/end_point_type_check/{item_id}")
async def get_item(item_id: int): # whatever is converting the HTTP request to a function call is converting the {item_id} string to an intege 
    return {"item_int": item_id}

@app.get("/end_point_no_type_check/{item_id}")
async def get_item(item_id): # whatever is converting the HTTP request to a function call is converting the {item_id} string to an intege 
    return {"item_int": item_id} # both ur: end_point_no_type_check/foo and end_point_no_type_check/3 would work


# it is possible to create an api that would accept input only from a predefined set of values
# didn't know that Enum existed in Python
from enum import Enum
class PathParameterValue(str, Enum):
    v1 = 'v1'
    v2 = 'v2'
    v3 = 'v3'

@app.get('/enum/{enum_value}')
async def get_enum(enum_value: PathParameterValue):
    if enum_value == PathParameterValue.v1:
        return {"message": "damn !!"}

    if enum_value == PathParameterValue.v2:
        return {"message": "wow !!"}

    return {"message": "really ??"}


# fast api supports file paths as path parameters: https://fastapi.tiangolo.com/tutorial/path-params/#path-convertor


# it is possible to work with query parameters as well
# query_param1 and query_param2 are known to be query parameters because there are not in the path description
@app.get('/endpoint/{path_param1}')
async def endpoint_func(path_param1: str, query_param1: str, query_param2: int): # just in any usual python function we can set the default values and so on.. 
    return {"path_param": {path_param1}, 
            "q_param1": query_param1, 
            "q_param2": query_param2}



# to work with the request body, the request body is expected to represent the parameters of some data model
from pydantic import BaseModel


class MyDataModel(BaseModel):
    first_name: str
    last_name: str 
    height: float | None = None # check pydantic for a better idea on the syntax...


@app.post('/post_endpoint')
async def item_endpoint(item: MyDataModel):
    # this simple call will compare the json in the request body to 'MyDataModel' model, validate
    # and then convert it into a class instance
    return item



@ app.get('/ex_endpoint')
async def endpoint(q: Annotated[str | None, Query(min_length=2, max_length=20)]): # this is required since the I did not set a default value. We can set a default value as '...' to let fastAPI know it is required 
    return {"re"}


# so basically when it comes to request bodies, fastapi use pydantic the same way 'Django' uses serializers

from datetime import date


class DateModelBase(BaseModel):
    first_name: str
    last_name: str


class DataModelIn(DateModelBase):
    birth_date: date


# we are considerate of the user' private data so we don't return the date of birth
class DataModelOut(DateModelBase):
    pass


@app.post("/data_model") 
def endpoint(data_obj: Annotated[DataModelIn, Body()], show_date: Annotated[bool, Query()]=False):
    if show_date:
        return {"message": "object received successfully", 
            "output_obj": DataModelIn(**data_obj.model_dump())}

    return {"message": "object received successfully", 
        "output_obj": DataModelOut(**data_obj.model_dump())}
