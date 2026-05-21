from fastapi import FastAPI, HTTPException, status, Path
from typing import Optional
from pydantic import BaseModel
app = FastAPI()

users = {
    1 :{
        "name":"Reginald Ankomah",
        "school":"KNUST",
        "age":18,
        "programme":"Information Technology",
        "contact":"0503952091"

    },
    2 :{
        "name":"John Sarbah",
        "school":"KNUST",
        "age":19,
        "programme":"Computer Science",
        "contact": "0549758751"
    },
    3 :{
        "name":"Elspeth",
        "school":"KNUST",
        "age":17,
        "programme":"Computer Engineering",
        "contact": "0258085033"
    },
    4 :{
        "name":"David Goliath",
        "school":"KNUST",
        "age":18,
        "programme":"Biomedical Engineering",
        "contact": "0247584963"
    },
    5 :{
        "name":"Judy Johns",
        "school":"KNUST",
        "age":21,
        "programme":"Medicine",    
        "contact": "0508180968"

    }
}

#Base Pydantic Models
class User(BaseModel):
    name:str
    school:str
    age:int
    programme:str
    contact:str

class UpdateUser(BaseModel):
    name:Optional[str] = None
    school:Optional[str] = None
    age:Optional[int] = None
    programme:Optional[str] = None
    contact:Optional[str] = None

#Endpoint
@app.get("/")
def root():
    return {"message":"Welcome to fastAPI"}

#Get USers
@app.get("/users/{user_id}")
def get_user(user_id:int = Path(..., description="The ID demanded", gt=0, lt=100)):
    if user_id not in users:
        raise HTTPException(status_code=404, 
                            detail="User Not Found!")
    return users[user_id]

#create a user
@app.post("/users/{user_id}", status_code=status.HTTP_201_CREATED)
def create_user(user_id:int, user:User):
    if user_id in users:
        raise HTTPException(status_code=400, 
                            detail="User already exists")

    users[user_id] = user.dict()
    return user

#update a user
@app.put("/users/{user_id}")
def update_user(user_id:int, user:UpdateUser):
    if user_id not in users:
        raise HTTPException(status_code=404, 
                            detail="User not here")
    
    current_user = users[user_id]

    if user.name is not None:
        current_user["name"] = user.name
    if user.school is not None:
        current_user["school"] = user.school
    if user.age is not None:
        current_user["age"] = user.age
    if user.programme is not None:
        current_user["programme"] = user.programme
    if user.contact is not None:
        current_user["contact"] = user.contact

    return current_user

# delete a user
@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    if user_id not in users:
        raise HTTPException(status_code=404, 
                            detail="User not here")
    
    deleted_user = users.pop(user_id)
    return{"Message":"User has been deleted", "deleted_user": deleted_user}

# search for a user
@app.get("/user/search/")
def search_by_name(name: Optional[str] = None):
    if not name:
        return {"message":"Name parameter is required"}
    
    for user in users.values():
        if user["name"].lower() == name.lower():
            return user
    raise HTTPException(status_code=404, 
                        detail="User not found!")
