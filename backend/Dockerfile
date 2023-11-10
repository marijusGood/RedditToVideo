FROM arm64v8/python:3.10

WORKDIR /code
RUN apt update && apt upgrade -y 
RUN apt install -y build-essential
RUN apt install -y libyaml-dev
RUN pip install --upgrade pip setuptools
RUN pip install Cython
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Update and install system dependencies

RUN rm -f /etc/ImageMagick-6/policy.xml

RUN apt install -y ffmpeg libsndfile1 ghostscript
# Copy your source code
COPY . /code

# Copy policy.xml for ImageMagick
RUN cp policy.xml /etc/ImageMagick-6/policy.xml


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
