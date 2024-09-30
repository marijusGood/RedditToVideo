from googleVoice import googleVoice
from reddit import Reddit
import random
import re
from PIL import Image
import numpy as np
import librosa
import time
import json
import soundfile as sf
from moviepy.editor import *
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os

class Video:

    def writeToJSON(self, text, video_name, filename='errors.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("File not found")

        data[video_name] = text
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        

    def cutAudio(self, audio_text, start, end):
        audio, sr = librosa.load(f"{audio_text}.mp3", sr=None)
        duration = len(audio)

        cut_time_start = int(start * sr)
        cut_time_end = int(end * sr)
        cut_audio = audio[cut_time_start:duration - cut_time_end]

        sf.write(f"{audio_text}.mp3", cut_audio, sr)

    def split_sentences(self, text):
        # Check if there are any sentence-ending punctuations in the text
        if re.search('[.!?]', text):
            # If there are, split the text into sentences
            sentences = re.findall(r'[^.!?]*[.!?]', text)
        else:
            # If there aren't, return the original text as a single-item list
            sentences = [text]
        
        return sentences

    def subreddit(self, subreddit, AIvoiceNumber, video_name, image = "reddit.png"):
        reddit = Reddit()

        try:
            intro_text, text_list = reddit.getSubreddit(subreddit)
            self.createVideo(intro_text, text_list, image, AIvoiceNumber, video_name)
        except Exception as e:
            self.writeToJSON(e, video_name)
        
        

    def customVideo(self, title, answers, AIvoiceNumber, video_name, image = "reddit.png"):
        self.createVideo(title, [answers], image, AIvoiceNumber, video_name)
    
    def customPost(self, url, AIvoiceNumber, video_name, image = "reddit.png"):
        reddit = Reddit()

        try:
            intro_text, text_list = reddit.getCustomPost(url)
            self.createVideo(intro_text, text_list, image, AIvoiceNumber, video_name)
        except Exception as e:
            self.writeToJSON(e, video_name)
        
        

    def createVideo(self, intro_text, text_list, image, AIvoiceNumber, video_name):

        text_clips = []
        audio_durations = []
        audio_files = []
        audio_list = []
        sr_list = []

        voice = googleVoice()

        temp = []
        count_words = 0
        for text in text_list:
            words = text.split(" ")
            if(count_words + len(words) < 160):
                count_words += len(words)
                sentence = self.split_sentences(text)
                for i in sentence:
                    if (len(i) > 0 and len(i) < 100):
                        temp.append(i.replace('\n', '').replace('.', '').replace('!', '').replace('?', ''))
                    elif (len(i) > 0):
                        sentence_words = i.split(" ")
                        temp_sentence = ""
                        
                        for k, count in zip(sentence_words, range(len(sentence_words))):
                            if (len(k) > 0):
                                temp_sentence += " " + k
                                if(count % 10 == 0 and count != 0):
                                    if(len(sentence_words) - count < 5):
                                        for j in range(1, len(sentence_words) - count):
                                            temp_sentence += " " + sentence_words[count + j]

                                    temp.append(temp_sentence[1:].replace('\n', '').replace('.', '').replace('!', '').replace('?', ''))
                                    temp_sentence = ""
                                    if(len(sentence_words) - count < 5):
                                        break
                        if(len(temp_sentence) > 0):
                            temp.append(temp_sentence)
                
            else:
                break
            temp.append("silence_pause")


        text_list = temp
        voice.getVoice(intro_text, "intro.mp3", AIvoiceNumber)
        self.cutAudio("intro", 0.1, 0.1)
        audio, sr = librosa.load("intro.mp3", sr=None)
        audio_list.append(audio)
        sr_list.append(sr)


        #intro_text, text_list = 'this is the intro this is the intro this is the intro intro this is the intro', ['That prisoner who became a model from a mugshot', ' Don’t think he would have been give a lesser sentence AND a career if he was ugly', 'silence_pause', 'I have a good-looking business partner', ' We are constantly delegating tasks based on whether we need Sasquatch or Captain America', 'silence_pause', 'Go out broke and come home drunk', 'silence_pause', 'Anyone can ask, but attractive people are so much more likely to get help from strangers', ' Just a sad little twisted fact of life', 'silence_pause', 'I’ve had one of my friends get rejected because the girl', 'found the best friend of that guy (me) to be too ugly', ' My friend got rejected because IM UGLY', 'silence_pause', 'get out of prison for a felony, immediately get a modeling contract and start dating an heiress', 'silence_pause', 'A girl just drove 3 hours to fuck my room mate', ' They never really spoke or met before this', ' Blew my mind', 'silence_pause', 'Always having dating options', ' Not actively seeking out potential partners', ' Potential partners seek them out', 'silence_pause', 'I wouldn’t know', ' I am handsome', 'silence_pause', 'People will go completely out of their way to do things for them', ' Moving', ' Something broke', ' Card declined', ' Someone will help them', 'silence_pause', 'Yeah, its called the halo effect', ' We tend to assume attractive people are nicer and smarter', 'silence_pause']


        audio = AudioFileClip("intro.mp3")
        duration = audio.duration - 0.04
        text_clip = TextClip(intro_text, fontsize=50, color='black', stroke_color='black', stroke_width=3, font='Arial-Bold', size=(608, 700), align="south", method="caption", bg_color='white')
        text_clip = text_clip.set_duration(duration).set_position(('center', 'top'))

        image = os.path.abspath(image)
        image = Image.open(image).convert("RGBA")
        image_np = np.array(image)

        # If the image is grayscale (2D array), convert it to RGB
        if len(image_np.shape) == 2:
            image_np = np.stack((image_np,) * 3, axis=-1)

        # If the image is RGB (3D array without alpha channel), add an alpha channel
        if image_np.shape[2] == 3:
            image_np = np.concatenate([image_np, 255 * np.ones((*image_np.shape[:2], 1), dtype=np.uint8)], axis=2)

        image_clip = ImageClip(image_np, transparent=True)

        desired_width = 608  
        max_height = int(0.4 * 1000)
        aspect_ratio = image_clip.size[0] / image_clip.size[1]
        new_height = int(desired_width / aspect_ratio)


        if new_height > max_height:
            new_height = max_height
            desired_width = int(new_height * aspect_ratio)
        
        image_clip = image_clip.resize(height=new_height, width=desired_width)
        image_clip = image_clip.set_duration(duration).set_position(('center', 'top'))

        # Create a white background clip
        #background_clip = ColorClip(size=text_clip.size, col=(255, 255, 255)).set_duration(duration)
        #background_clip = background_clip.set_position(('center', 'top'))
        combined_clip = CompositeVideoClip([text_clip, image_clip])

        text_clips.append(combined_clip)
        audio_durations.append(duration)

        #generate silence
        sr = 44100
        silence = np.zeros(int(sr * 0.3))
        sf.write("silence.mp3", silence, sr)


        for i, text in enumerate(text_list):
            if text == "silence_pause":
                text = " "
                audio, sr = librosa.load("silence.mp3", sr=None)
                audio_list.append(audio)
                sr_list.append(sr)
                duration = 0.3
                text_clip = TextClip(text, fontsize=70, color='white', stroke_color='black', stroke_width=3.5, kerning=-4, font='Arial-Bold', size=(650, 900), align="center", method="caption", bg_color='transparent')
            
                text_clip = text_clip.set_duration(duration).set_position(('center', 'center'))
                
                
                # Append the text clip, audio duration, and audio file to their respective lists
                text_clips.append(text_clip)
                audio_durations.append(duration)
                continue



            voice.getVoice(text, f"temp_audio{i}.mp3", AIvoiceNumber)
            time.sleep(1)
            self.cutAudio(f"temp_audio{i}", 0.1, 0.1)
            audio, sr = librosa.load(f"temp_audio{i}.mp3", sr=None)
            audio_list.append(audio)
            sr_list.append(sr)

            audio = AudioFileClip(f"temp_audio{i}.mp3")
            
            duration = audio.duration
    
            text_clip = TextClip(text, fontsize=80, color='white', stroke_color='black', stroke_width=3.5, kerning=-4, font='Arial-Bold', size=(540, 900), align="center", method="caption", bg_color='transparent')
            
            text_clip = text_clip.set_duration(duration).set_position(('center', 'center'))
            
            text_clips.append(text_clip)
            audio_durations.append(duration)

        output = np.concatenate(audio_list)

        # Export result
        sf.write("comments.mp3", output, sr_list[0])
        audio = AudioFileClip("comments.mp3")
        audio_files.append(audio)

        final_video = concatenate_videoclips(text_clips)

        rand_num = random.randint(0, 120)

        video = VideoFileClip("pk.mp4").subclip(rand_num, rand_num+80)
        video = video.without_audio()
        final_video = CompositeVideoClip([video, final_video])
        combined_audio = concatenate_audioclips(audio_files)
        final_video = final_video.set_audio(combined_audio)
        total_duration = sum(audio_durations)
        final_video = final_video.set_duration(total_duration)
        final_video.write_videofile(f"{video_name}.mp4", codec="mpeg4", audio_codec="libmp3lame")

        for i in range(len(text_list)):
            try:
                os.remove(f"temp_audio{i}.mp3")
            except Exception as e:
                pass
        os.remove("intro.mp3")
        os.remove("comments.mp3")
        self.writeToJSON("done", video_name)