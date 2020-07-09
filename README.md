# A Simple Keras + deep learning REST API with DASH from Plotly

This repository contains the code from [*Building a simple Keras + deep learning REST API*](https://blog.keras.io/building-a-simple-keras-deep-learning-rest-api.html), published on the Keras.io blog.

And integrates with Dash plotly https://github.com/plotly/dash-simple-image-processor

## Getting started


You can now access the REST API via `http://127.0.0.1:5000`.

## Submitting requests to the Keras server

Requests can be submitted via cURL:

```sh
$ curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
{
  "predictions": [
    {
      "label": "beagle", 
      "probability": 0.9901360869407654
    }, 
    {
      "label": "Walker_hound", 
      "probability": 0.002396771451458335
    }, 
    {
      "label": "pot", 
      "probability": 0.0013951235450804234
    }, 
    {
      "label": "Brittany_spaniel", 
      "probability": 0.001283277408219874
    }, 
    {
      "label": "bluetick", 
      "probability": 0.0010894243605434895
    }
  ], 
  "success": true
}
```

Or programmatically:

```sh
$ python simple_request.py 
1. beagle: 0.9901
2. Walker_hound: 0.0024
3. pot: 0.0014
4. Brittany_spaniel: 0.0013
5. bluetick: 0.0011
```
This Project is Funded by Athinoula A. Martinos Center for Biomedical Imaging
