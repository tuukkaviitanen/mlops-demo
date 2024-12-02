# Crypto Predict API

> Demo about using [GitHub Actions](https://docs.github.com/en/actions) as a [MLOps](https://www.databricks.com/glossary/mlops) tool

- **Running live at: https://crypto-predictor-08ot.onrender.com**
  - Running as a free tier service, so it takes some time to start responding
  - Has [Swagger UI](https://swagger.io/tools/swagger-ui/) documentation with instructions

## Summary

- Teaches a machine learning model from real-time data, that predicts the price of [Bitcoin](https://bitcoin.org/en/) at a specific time
- Wraps the model inside a [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) [API](https://www.ibm.com/topics/api)
- Creates a [Docker](https://www.docker.com/) image out of the API with descriptive tags
- Deploys the latest image to [Render](https://render.com/)
- Does all of this in a GitHub Actions workflow every 6 hours to always keep the model trained with the latest data

## Model training

- Uses real-time updating history data from [Alpaca Markets](https://alpaca.markets/) [Market Data API](https://docs.alpaca.markets/docs/about-market-data-api) using their [official Python SDK](https://github.com/alpacahq/alpaca-py)
- Teaches a [machine learning model](https://www.coursera.org/articles/machine-learning-models) with [Facebook prophet](https://facebook.github.io/prophet/)
- Saves the model as a [pickle](https://docs.python.org/3/library/pickle.html) binary-file on the disk

## API

- [Flask API](https://flask.palletsprojects.com/en/3.0.x/) served with [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/index.html)
- The function is to use the model from any other application using the API over [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
  - This [microservice structure](https://microservices.io/) allows the usage of the model even when the user application is created using different technologies
  - This also allows the model to be retrained or updated without needing to update the user applications
- The API is run loads the binary model at startup
- Listens to `/bitcoin` endpoint that takes `date` query parameter
  - Example: `/bitcoin?date=2024-06-01`
  - Uses the `date` parameter to run it through the model and returns the predicted price in the following [JSON](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON) format:
    ```
    {
      "date": "Sat, 01 Jun 2024 00:00:00 GMT",
      "prediction": 56771.779953588826,
      "prediction low": 53746.06414094623,
      "prediction_high": 60034.61668451781
    }
    ```
- [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is enabled, so the API can be called from other web applications
  - [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/) is used to simplify this process

## Dockerfile

- Uses [Multi-stage dockerfile](https://docs.docker.com/build/building/multi-stage/)
- Trains the model in the build stage
- Only model binary, API python file and the API's dependencies are applied to the final image
  - This reduces the final image size and potentially reduces the [attack surface](https://www.fortinet.com/resources/cyberglossary/attack-surface)

## GitHub Actions workflow

- Runs on push to main branch and on a [CRON schedule](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) every 6 hours
- Tags a new commit with a [semantic version](https://www.geeksforgeeks.org/introduction-semantic-versioning/)
  - If run with a schedule, commit is already tagged, so the existing version is just read
- Builds a [Docker image](https://docs.docker.com/guides/docker-concepts/the-basics/what-is-an-image/) using the [Dockerfile](Dockerfile) and publishes the image to [GitHub Container Registry (ghcr.io)](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) under this GitHub repository
  - The image is tagged with the following tags:
    - `latest` for finding the latest version of the image
    - The semantic version of the commit (e.g. `0.3.1`) for finding the latest image of this specific commit
    - The semantic version combined with the timestamp of the build (e.g. `0.3.1-20240518121047`) for having a unique identifier for each build, that also clearly states the software version and the build time
  - It's important to note that only one image can hold a specific tag at a time, and other images holding the same tags will lose those tags
- Triggers [Render](https://render.com/) deployment for the application
  - The Render web service is configured to run the image with the `latest` tag so it will always deploy the newly built image
    - This image deployment allows most of the configuring to be done in the repository and just minimal setup at Render side

## Setup

### Dependencies

- [Python](https://www.python.org/) 3.x
- Required Python dependencies
  - For running train script ([train.py](train.py))
    - [alpaca-py](https://pypi.org/project/alpaca-py/)
    - [prophet](https://pypi.org/project/prophet/)
  - For running the API ([api.py](api.py))
    - [Flask](https://pypi.org/project/Flask/)
    - [waitress](https://pypi.org/project/waitress/)
    - [pandas](https://pypi.org/project/pandas/)
    - [prophet](https://pypi.org/project/prophet/)
    - [flask-cors](https://pypi.org/project/Flask-Cors/)
  - For running the [Jupyter notebook](https://realpython.com/jupyter-notebook-introduction/) machine learning experiment ([train.ipynb](train.ipynb))
    - [pandas](https://pypi.org/project/pandas/)
    - [prophet](https://pypi.org/project/prophet/)
    - [plotly](https://pypi.org/project/plotly/)
    - [statsmodels](https://pypi.org/project/statsmodels/)
    - [alpaca-py](https://pypi.org/project/alpaca-py/)
