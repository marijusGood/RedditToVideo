from typing import List, Optional
from fastapi import FastAPI, Form, UploadFile, File, Depends, Body
from pydantic import BaseModel, conint
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import uvicorn
import json
import os
from video import Video

class userModel(BaseModel):
    email: str
    AIvoice: str

class customVideo(userModel):
    title: str
    answers: str

class subredditModel(userModel):
    subreddit: str

class subredditUrlModel(userModel):
    url: str


app = FastAPI()
video = Video()
temp = "Something went wrong"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def file_stream():
        async with aiofiles.open("output_video.mp4", mode='rb') as f:
            while True:
                chunk = await f.read(1024)
                if not chunk:
                    break
                yield chunk

async def returnFile(temp):
    if os.path.exists("output_video.mp4"):
        return StreamingResponse(file_stream(), media_type="video/x-msvideo")
    else:
        return {"error": temp}

def removeFile():
    try:
        os.remove("output_video.mp4")
    except:
        pass

async def saveImage(image):
    image_content = await image.read()
    with open(image.filename, 'wb') as f:
        f.write(image_content)
    return image.filename


@app.post("/subreddit")
async def subreddit(input: str = Form(...), image: UploadFile = File(None)):
    input_data = json.loads(input)
    input_proccessed = subredditModel(**input_data)

    removeFile()
    
    try:
        if image is not None:
            await saveImage(image)
            temp = video.subreddit(input_proccessed.subreddit, input_proccessed.AIvoice, input_proccessed.filename)
        else:
            temp = video.subreddit(input_proccessed.subreddit, input_proccessed.AIvoice)

        return await returnFile(temp)
    except:
        return {"error": "Something went wrong"}

@app.post("/subredditpost")
async def subredditpost(input: str = Form(...), image: UploadFile = File(None)):
    input_data = json.loads(input)
    input_proccessed = subredditUrlModel(**input_data)

    removeFile()

    try:
        if image is not None:
            await saveImage(image)
            temp = video.customPost(input_proccessed.url, input_proccessed.AIvoice, input_proccessed.filename)
        else:
            temp = video.customPost(input_proccessed.url, input_proccessed.AIvoice)

        return await returnFile(temp)
    except:
        return {"error": "Something went wrong"}


@app.post("/customvideo")
async def customvideo(input: str = Form(...), image: UploadFile = File(None)):

    input_data = json.loads(input)
    input_proccessed = customVideo(**input_data)
    
    removeFile()
    
    try:
        if image is not None:
            filename = await saveImage(image)
            video.customVideo(input_proccessed.title, input_proccessed.answers, input_proccessed.AIvoice, filename)
        else:
            video.customVideo(input_proccessed.title, input_proccessed.answers, input_proccessed.AIvoice)

        # Your logic to return a file
        return await returnFile(temp)
    except:
        return {"error": "Something went wrong"}
