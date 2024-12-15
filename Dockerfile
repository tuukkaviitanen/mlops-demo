FROM python:3.13-bookworm AS build-stage

WORKDIR /usr/src/app

# Install only training deps
RUN pip install \
    alpaca-py==0.33.1 \
    prophet==1.1.6 \
    kaleido==0.2.1

COPY ./train.py ./

# Build model
RUN python train.py

# Swagger UI builder for fetching latest Swagger UI files
FROM swaggerapi/swagger-ui:v5.17.14 AS swagger-builder

# Remove searchbar/topbar
RUN sed -i 's#SwaggerUIStandalonePreset#SwaggerUIStandalonePreset.slice(1)#' /usr/share/nginx/html/swagger-initializer.js
# Replace default doc with local doc
RUN sed -i 's#https://petstore.swagger.io/v2/swagger.json#/openapi.yaml#' /usr/share/nginx/html/swagger-initializer.js
RUN sed -i 's#Swagger UI#Crypto predictor#' /usr/share/nginx/html/index.html

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

# Copy Swagger UI files
COPY --from=swagger-builder /usr/share/nginx/html ./static
COPY ./openapi.yaml ./static/openapi.yaml

# Copy figs
COPY --from=build-stage /usr/src/app/fig* ./static/

# Run API with unbuffered text output (no need to flush)
CMD ["python", "-u", "api.py"]
