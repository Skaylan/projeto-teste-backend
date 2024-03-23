FROM python:latest

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# RUN flask db init
# RUN flask db migrate -m "initial migration"
# RUN flask db upgrade
CMD [ "python", "run.py" ]