from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, List
import json
import uvicorn
import os

# Load Discourse posts
with open("discourse_posts.json", "r") as f:
    discourse_posts = json.load(f)

# Data model for input
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 image string, not used here

# Data model for output
class AnswerResponse(BaseModel):
    answer: str
    links: List[dict]

# Create FastAPI app
app = FastAPI()

# Utility to find relevant answers
def search_posts(question):
    matches = []
    question_lower = question.lower()
    for post in discourse_posts:
        title = post.get("title", "").lower()
        content = post.get("content", "").lower()
        url = post.get("url", "")

        if question_lower in title or question_lower in content:
            matches.append({
                "url": url,
                "text": title or content[:100]
            })
            if len(matches) >= 2:  # Return top 2
                break
    return matches

# Main API endpoint
@app.post("/api/", response_model=AnswerResponse)
def answer_question(data: QuestionRequest):
    question = data.question
    matches = search_posts(question)

    if matches:
        answer = f"I found {len(matches)} relevant post(s) on Discourse."
    else:
        answer = "Sorry, I couldn't find a relevant Discourse post."

    return {"answer": answer, "links": matches}
