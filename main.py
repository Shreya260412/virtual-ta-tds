from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

with open("posts.json") as f:
    POSTS = json.load(f)

class Query(BaseModel):
    question: str
    image: str = None  # optional

@app.post("/api/")
def answer_question(query: Query):
    question = query.question.lower()
    matches = []

    for post in POSTS:
        if any(word in post["content"].lower() for word in question.split()):
            matches.append({
                "url": post["url"],
                "text": post["title"]
            })

    if matches:
        return {
            "answer": "This may help based on past forum discussions.",
            "links": matches[:3]
        }
    else:
        raise HTTPException(status_code=404, detail="No relevant answer found.")
