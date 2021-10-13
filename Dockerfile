FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
RUN apt-get update && \
    apt-get install postgresql --yes
COPY . .
RUN chmod +x ./entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "-w 4","-b 0.0.0.0:8000", "CoinsApp.wsgi:application"]
