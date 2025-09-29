FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

    #http://localhost:8000/docs
    #http://127.0.0.1:8000/docs
    #docker build -t hotel-api .
    #docker run -p 8000:8080 hotel-api   
    #Map port 8080 inside the container to port 8000 on your host machine
    # Your app is listening on 0.0.0.0:8080 inside the container.
    # Your Docker host is listening on localhost:8000.