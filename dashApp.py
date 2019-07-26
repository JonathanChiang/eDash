import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import os
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
import datetime
from dash.dependencies import Input, Output, State
import dash_table
import pandas as pd

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['/Users/jonc101/Documents/Biomedical_Data_Science/deep_neuro.css']

server = Flask(__name__)
app = dash.Dash(server=server,external_stylesheets=external_stylesheets,static_folder='static')
app.title = "MGH Martinos Lab"

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

df = pd.read_csv('/Users/jonc101/Documents/Biomedical_Data_Science/deep_neuro.csv')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.Img(src=app.get_asset_url("deep_neuro.png")),
    html.Br(),
    html.Img(src=app.get_asset_url("model_inference_icon.png")),
    html.Br(),
    dcc.Link('Upload your Files', href='/page-1',
    style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}),
    html.Br(),
    html.Img(src=app.get_asset_url("model_inference_icon.png")),
    html.Br(),
    # you can use markdown here as well (dcc.markdown)
    dcc.Link('View Results', href='/page-2',
    style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold'}),
    dcc.Markdown(children=markdown_text),
])

page_1_layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.H1('Image Inverter'),
        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
            dcc.Tab(label='Image', value='tab-1-example'),
            dcc.Tab(label='Processed Image', value='tab-2-example'),
        ]),

        html.Div(id='tabs-content-example'),
    dcc.Link('Go back to home', href='/')
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.H3('Original Image'),
            html.Div(id='output-image-upload'),
            html.Br(),
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Converted Image'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])


def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename'),
               State('upload-image', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


page_2_layout =  dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("rows"),
)

'''
KEEP
'''

@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)

@server.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(server.root_path, 'static'),
                               'favicon.ico', mimetype='assets/favicon.ico')

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, port = 5050)
