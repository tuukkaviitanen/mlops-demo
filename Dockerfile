# Build stage
FROM python:3.9 AS build-stage

WORKDIR /usr/src/app

# Install training deps

RUN pip install alpaca-py prophet

# Build training file

COPY ./train.py ./

RUN python train.py

# Final stage

FROM python:3.9

WORKDIR /usr/src/app

# Install API deps

RUN pip install Flask waitress pandas prophet

# Copy API file

COPY ./api.py ./

# Copy model from build stage
COPY --from=build-stage /usr/src/app/model.pkl ./

CMD ["python", "-u", "api.py"]
