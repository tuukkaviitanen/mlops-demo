# Crypto Predict API

> Demo about using GitHub Actions as a MLOps tool

## Summary

- Teaches a machine learning model from real-time data, that predicts the price of Bitcoin at a specific time
- Wraps the model inside a web API
- Creates a Docker image out of it with descriptive tags
- Deploys the latest image to Render
- Does all of this in a GitHub Actions workflow every 6 hours



## Setup

- Install Python 3.x
- Install following dependencies
```
pip install alpaca-py
pip install statsmodels
pip install prophet
pip install plotly
pip install Flask
pip install waitress
pip install pandas
```
