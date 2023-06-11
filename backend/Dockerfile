FROM python:3.10

WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN apt update && apt upgrade -y && apt -y install ghostscript
RUN rm -f /etc/ImageMagick-6/policy.xml

COPY . /code

RUN cp policy.xml /etc/ImageMagick-6/policy.xml

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

#uvicorn app.main:app --host 0.0.0.0 --port 80
