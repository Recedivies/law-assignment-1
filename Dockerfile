# pull the official docker image
FROM python:3.8-alpine

# set work directory
WORKDIR /app/backend

# set env variables
ARG DATABASE_PROD_NAME
ARG DATABASE_PROD_USERNAME
ARG DATABASE_PROD_PASSWORD
ARG DATABASE_PROD_HOST
ARG SECRET_KEY
ARG ENVIRONMENT
ARG DJANGO_SETTINGS_MODULE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DATABASE_PROD_NAME ${DATABASE_PROD_NAME}
ENV DATABASE_PROD_USERNAME ${DATABASE_PROD_USERNAME}
ENV DATABASE_PROD_PASSWORD ${DATABASE_PROD_PASSWORD}
ENV DATABASE_PROD_HOST ${DATABASE_PROD_HOST}
ENV SECRET_KEY ${SECRET_KEY}
ENV ENVIRONMENT ${ENVIRONMENT}
ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE}

# install dependencies
COPY requirements.txt .

# Install required libraries and Python dependencies
RUN  \
    apk update && \
    apk upgrade && \
    apk add --no-cache bash postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install --upgrade pip -r requirements.txt && \
    apk --purge del .build-deps

# Add the rest of the code
COPY . .
# Copy scripts to main directory
COPY ./scripts/ /app/

# Make port 8000 available for the app
ENV PORT 8000
EXPOSE 8000

# Be sure to use 0.0.0.0 for the host within the Docker container,
# otherwise the browser won't be able to find it
RUN ["chmod", "+x", "/app/entrypoint.sh"]
ENTRYPOINT [ "/app/entrypoint.sh" ]