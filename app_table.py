import dash
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import os

# USAGE
# python simple_request.py

# import the necessary packages
import requests

# initialize the Keras REST API endpoint URL along with the input
# image path
KERAS_REST_API_URL = "http://localhost:5000/predict"


script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in


app = dash.Dash( external_stylesheets=[dbc.themes.BOOTSTRAP])
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

app.layout = html.Div([
	dcc.Upload(
		id='upload-data',
		children=html.Div([
			html.A('Run Inference')
		]),
		style={
			'width': '50%',
			'height': '60px',
			'lineHeight': '60px',
			'borderWidth': '1px',
			'borderStyle': 'dashed',
			'borderRadius': '5px',
			'textAlign': 'center'
		},
		multiple=False
	),
	html.Div(id='output-data-upload')
])

@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
			 [dash.dependencies.Input('upload-data', 'contents'),
			  dash.dependencies.Input('upload-data', 'filename')])




def update_output(contents, filename):
	if contents is not None:
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "/" + filename
		IMAGE_PATH = script_dir + rel_path



	# load the input image and construct the payload for the request
		image = open(IMAGE_PATH, "rb").read()
		payload = {"image": image}

		# submit the request
		r = requests.post(KERAS_REST_API_URL, files=payload).json()

		# ensure the request was sucessful
		if r["success"]:
			# loop over the predictions and display them
			df = pd.json_normalize(r["predictions"])
			df["probability"] = 100 * df["probability"]
			df = df.round({'probability': 2})
			df = df.rename(str.upper, axis='columns')

			return html.Div([
				html.Hr(),
				html.Img(src=contents),
				html.Hr(),
				dash_table.DataTable(
					id='table',
					columns=[{"name": i, "id": i} for i in df.columns],
					data=df.to_dict("rows"),
					style_cell={'width': '25px',
					'fontSize':20, 
					'font-family':'sans-serif',
					'height': '50px',
					'color' : 'black',
					'textAlign': 'center'}
				),

				],style={'columnCount': 1})

		# otherwise, the request failed
		else:
			print("Request failed")



if __name__ == "__main__":
    app.run_server(debug=True,threaded=True)
