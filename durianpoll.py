import os
from fastapi import FastAPI, Body
from pymongo import MongoClient
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["poll_db"]
collection = db["durian_poll"]

class VoteRequest(BaseModel):
    choice: str

@app.post("/poll")
def create_poll():
    poll_data = {
        "pollName": "durian-vote",
        "options": {
            "เนื้อแข็ง กรอบ": 0,
            "กรอบนอก นุ่มใน": 0,
            "เนื้อฉ่ำเละ": 0, 
            "ไม่กินทุเรียน": 0 
        }
    }

    result = collection.insert_one(poll_data)

    return {
        "message": "poll success",
    }
    
@app.get("/readpoll")
def get_poll():
    data = collection.find_one({}, {"_id": 0})
    return {"result": data}

@app.post("/vote")
def vote_poll(data: VoteRequest):
    choice = data.choice

    poll = collection.find_one({"pollName": "durian-vote"}, {"_id": 0})

    if choice not in poll["options"]:
        return {"message": "not found choice"}

    result = collection.update_one(
        {"pollName": "durian-vote"},
        {"$inc": {f"options.{choice}": 1}}
    )

    return {"message": f"vote for '{choice}' success"}