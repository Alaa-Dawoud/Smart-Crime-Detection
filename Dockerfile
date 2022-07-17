FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt-get update
RUN apt install -y libgl1-mesa-glx

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]