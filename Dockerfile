# Use the official lightweight Python image.
FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./requirements.txt $APP_HOME/requirements.txt
# Install production dependencies.
RUN pip install -r requirements.txt

COPY . ./

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  app.main:app 