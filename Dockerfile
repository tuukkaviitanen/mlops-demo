FROM python:3.13-bookworm AS build-stage

WORKDIR /usr/src/app

# Install only training deps
RUN pip install \
    alpaca-py==0.33.1 \
    prophet==1.1.6

COPY ./train.py ./

# Build model
RUN python train.py

FROM python:3.13-bookworm AS final-stage

WORKDIR /usr/src/app

# Install only model usage & API deps
RUN pip install \
    flask==3.1 \
    flask_cors==5.0.0 \
    waitress==3.0.2 \
    pandas==2.2.3 \
    prophet==1.1.6

COPY ./api.py ./

# Copy packaged model from build stage
COPY --from=build-stage /usr/src/app/model.pkl ./

# Run API with unbuffered text output (no need to flush)
CMD ["python", "-u", "api.py"]
