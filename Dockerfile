FROM python:3.10.12
WORKDIR /app
COPY  . . 
RUN pip install -r requirements.txt
EXPOSE  8001
CMD ["python", "src/main.py"]