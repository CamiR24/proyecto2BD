FROM python:3.11
WORKDIR /app
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ /app

EXPOSE 8501

CMD [ "streamlit", "run", "main.py", "--server.address=0.0.0.0"]

