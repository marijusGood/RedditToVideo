from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop

clip = VideoFileClip("output.mp4")

# Specify new dimensions
new_height = 1080  # height for 1080p
new_width = new_height * 9 // 16  # calculate width for 9:16 aspect ratio

# Resize first to maintain the height and then crop to maintain aspect ratio
resized_clip = clip.resize(height=new_height)

# Crop the video
cropped_clip = resized_clip.fx(crop, x_center=resized_clip.w/2, y_center=resized_clip.h/2, width=new_width, height=new_height)

final_clip = cropped_clip.without_audio()

final_clip.write_videofile("output1.mp4")
