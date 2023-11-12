from typing import List, Optional
from fastapi import FastAPI, Form, UploadFile, File, Depends, Body, BackgroundTasks
from pydantic import BaseModel, conint
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import aiofiles
import uvicorn
import json
import os
from video import Video
import random
import string

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

async def file_stream(path):
        async with aiofiles.open(f"{path}.mp4", mode='rb') as f:
            while True:
                chunk = await f.read(1024)
                if not chunk:
                    break
                yield chunk

async def returnFile(path):
    if os.path.exists(f"{path}.mp4"):
        return StreamingResponse(file_stream(path), media_type="video/x-msvideo")


def removeFile():
    prefix = "video-"
    for filename in os.listdir('.'):
        if filename.startswith(prefix):
            os.remove(filename)
            print(f"Removed: {filename}")

async def saveImage(image):
    image_content = await image.read()
    with open(image.filename, 'wb') as f:
        f.write(image_content)
    return image.filename


@app.post("/subreddit")
async def subreddit(background_tasks: BackgroundTasks, input: str = Form(...), image: UploadFile = File(None)):
    input_data = json.loads(input)
    input_proccessed = subredditModel(**input_data)
    video_name = "video-" + generate_random_string()
    removeFile()
    
    try:
        if image is not None:
            await saveImage(image)
            background_tasks.add_task(video.subreddit, input_proccessed.subreddit, input_proccessed.AIvoice, video_name, input_proccessed.filename)
            #temp = video.subreddit(input_proccessed.subreddit, input_proccessed.AIvoice, input_proccessed.filename)
        else:
            background_tasks.add_task(video.subreddit, input_proccessed.subreddit, input_proccessed.AIvoice, video_name)
            #temp = video.subreddit(input_proccessed.subreddit, input_proccessed.AIvoice)

        return {"video_name": str(video_name)}
    except Exception as e:
        print(e)
        error_message = str(e)
        return {"error": error_message}

@app.post("/subredditpost")
async def subredditpost(background_tasks: BackgroundTasks, input: str = Form(...), image: UploadFile = File(None)):
    input_data = json.loads(input)
    input_proccessed = subredditUrlModel(**input_data)
    video_name = "video-" + generate_random_string()
    removeFile()

    try:
        if image is not None:
            await saveImage(image)
            background_tasks.add_task(video.customPost, input_proccessed.url, input_proccessed.AIvoice, video_name, input_proccessed.filename)
            #temp = video.customPost(input_proccessed.url, input_proccessed.AIvoice, input_proccessed.filename)
        else:
            background_tasks.add_task(video.customPost, input_proccessed.url, input_proccessed.AIvoice, video_name)
            #temp = video.customPost(input_proccessed.url, input_proccessed.AIvoice)

        return {"video_name": str(video_name)}
    except Exception as e:
        print(e)
        error_message = str(e)
        return {"error": error_message}


@app.post("/customvideo")
async def customvideo(background_tasks: BackgroundTasks, input: str = Form(...), image: UploadFile = File(None)):

    input_data = json.loads(input)
    input_proccessed = customVideo(**input_data)
    video_name = "video-" + generate_random_string()
    removeFile()
    
    try:
        if image is not None:
            filename = await saveImage(image)
            background_tasks.add_task(video.customVideo, input_proccessed.title, input_proccessed.answers, input_proccessed.AIvoice, video_name, filename)
            #temp = video.customVideo(input_proccessed.title, input_proccessed.answers, input_proccessed.AIvoice, filename)
        else:
            background_tasks.add_task(video.customVideo, input_proccessed.title, input_proccessed.answers, input_proccessed.AIvoice, video_name)
            #temp = video.customVideo(input_proccessed.title, input_proccessed.answers, input_proccessed.AIvoice)

        # Your logic to return a file
        return {"video_name": str(video_name)}
    except Exception as e:
        print(e)
        error_message = str(e)
        return {"error": error_message}

@app.get("/get-video/{id}")
async def test(id: str):
    filename='errors.json'
    with open(filename, 'r') as file:
        data = json.load(file)
        print(data)
    if id in data:
        return {"error": data[id]}

    try:
        return await returnFile(id)
    except Exception as e:
        print(e)
        error_message = str(e)
        return {"error": error_message}


