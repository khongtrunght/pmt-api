FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY hust /app/hust
COPY resources /app/resources
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "5", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--timeout", "90"]