import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import os
import datetime
import dash_table
import pandas as pd
import glob
from io import BytesIO
from PIL import Image, ImageFile
from urllib.parse import quote as urlquote
from flask import Flask, send_from_directory
from dash.dependencies import Input, Output, State
import pydicom
import png
import numpy as np
# TODO
# CUSTOM CSS
# https://dash.plot.ly/external-resources

def pil_to_b64(im, enc_format='png', verbose=False, **kwargs):
    """
    Converts a PIL Image into base64 string for HTML displaying
    :param im: PIL Image object
    :param enc_format: The image format for displaying. If saved the image will have that extension.
    :return: base64 encoding
    """
    t_start = time.time()

    buff = _BytesIO()
    im.save(buff, format=enc_format, **kwargs)
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")

    t_end = time.time()
    if verbose:
        print(f"PIL converted to b64 in {t_end - t_start:.3f} sec")

    return encoded


def rotate(image_path, degrees_to_rotate, saved_location):
    """
    Rotate the given photo the amount of given degrees, show it and save it

    @param image_path: The path to the image to edit
    @param degrees_to_rotate: The number of degrees to rotate the image
    @param saved_location: Path to save the cropped image
    """
    image_obj = Image.open(image_path)
    rotated_image = image_obj.rotate(degrees_to_rotate)
    name_directory =  saved_location + "test" + ".png"
    rotated_image.save(name_directory)



#data['img'] = '''R0lGODlhDwAPAKECAAAAzMzM/////wAAACwAAAAADwAPAAACIISPeQHsrZ5ModrLl
#N48CXF8m2iQ3YmmKqVlRtW4MLwWACH+H09wdGltaXplZCBieSBVbGVhZCBTbWFydFNhdmVyIQAAOw=='''


def directory_flip(directory, out):
    list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(directory))]
    for filename in list_of_images:
        im=Image.open(directory + filename)
        im_rotate=im.rotate(180)
        im_rotate.save(out + 'rotated_' + filename)

print(dcc.__version__) # 0.6.0 or above is required

external_stylesheets = ['/Users/jonc101/Documents/Biomedical_Data_Science/deep_neuro.css']
# google  external_javascript:

server = Flask(__name__)
app = dash.Dash(server=server,external_stylesheets=external_stylesheets)
app.title = "MGH Martinos Lab"




markdown_text = '''

AIRIS: Artificially Intelligent Vision:
- [X] Lesion Detected
- [ ] Tumor Detected

'''

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

#df = pd.read_csv('/Users/jonc101/Documents/Biomedical_Data_Science/deep_neuro.csv')

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.Br(),
    html.A([
            html.Img(
                src=app.get_asset_url("mgh_stanford.png"),
                )
    ], href='/page-1'),

    html.Br(),

]),

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
#        html.Button(
#            'Run Operation',
#            id='button-run-operation',
#            style={'margin-right': '10px', 'margin-top': '5px'}
#        ),
        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
            dcc.Tab(label='Image', value='tab-1-example'),
            dcc.Tab(label='Processed Image', value='tab-2-example'),
        #    dcc.Tab(label='Processed Tables', value='tab-3-example'),
        ]),

        html.Div(id='tabs-content-example'),
    #dcc.Link('Go back to home', href='/')
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])

# upload thing:
#   contents
#   callback: that changed: given that a process change:
#       have that data be ready for submit callback for dropdown of functions:

def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div([
            html.Br(),
            dcc.Dropdown(
                id='image-dropdown',
                options=[
                {'label': 'Crop', 'value': 'crop'},
                {'label': 'Rotate 180', 'value': 'rotate'}
        ],
        value='rotate'
    ),
            html.Button(id='image-submit-button', n_clicks=0, children='Submit'),
            html.Div(id='output-image-upload'),
            html.Br(),
        ])
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('PreProcessed Results'),
            html.Div(id='output-image-upload', style={'display': 'inline-block'}),
            html.Div(html.Img(src = app.get_asset_url("data/mini_brain.png")))
#                        ), style={'display': 'inline-block'})
            #html.Div(dcc.Markdown(children=markdown_text), style={'display': 'inline-block'})
        ])

#    elif tab == 'tab-3-example':
#        return html.Div([
#            html.H3('PreProcessed Results'),
#            html.Div(html.Img(src = app.get_asset_url("data/test.png")), style={'display': 'inline-block'}),
#            html.Div(html.Img(src = app.get_asset_url("data/test.png")), style={'display': 'inline-block'}),


#        ])



@app.callback(
    dash.dependencies.Output('output-image-upload', 'children'),
    [dash.dependencies.Input('image-submit-button', 'n_clicks')],
    [dash.dependencies.State('image-dropdown', 'value'),
     dash.dependencies.State('upload-image', 'contents'),
     dash.dependencies.State('upload-image', 'filename'),
     dash.dependencies.State('upload-image', 'last_modified')
    ]
)

# create a dictionary to different functions:
# 180 numerical value:
# keys for dictionary
# callbacks get the function for this key:
# run function:
#


#def update_output_submit(click, angle, list_of_contents, list_of_names, list_of_dates):
#    if list_of_contents is not None:
#        im = []
#        for i in list_of_contents:
#            im_to_rotate=Image.open(BytesIO(base64.b64decode(i.split(',')[1])))
            # run this function as dropdown for im_to_rotate
            # im_to_rotate.XXXX
#            im_rotate=im_to_rotate.rotate(angle)
#            buffered = BytesIO()
#            im_rotate.save(buffered, format="png")
                #encoded = base64.b64encode(buff.getvalue()).decode("utf-8")

#            im.append('data:image/png;base64,{}'.format(base64.b64encode(buffered.getvalue()).decode("utf-8")))
        #print(im)
#        children = [
#            parse_contents(c, n, d) for c, n, d in
#            zip(im, list_of_names, list_of_dates)]
#        return children


def update_output_submit(click, func, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        im = []
        for i in list_of_contents:
            img=convert_dicom(i)
            img_transformed= pillow_function(img, func)
            buffered = BytesIO()
            img_transformed.save(buffered, format="png")
            im.append('data:image/png;base64,{}'.format(base64.b64encode(buffered.getvalue()).decode("utf-8")))
        children = [parse_contents(c, n, d) for c, n, d in zip(im, list_of_names, list_of_dates)]
        return children
    return ''

def convert_dicom(dc):
    file_data = dc.split(',')
    mime = file_data[0].split(':')[1].split(';')[0]
    file = BytesIO(base64.b64decode(file_data[1]))
    if mime == 'application/octet-stream':
        # if it's a png or jpeg already no need to process
        # this is all done in memory, no need to save the file
        raw = pydicom.filebase.DicomBytesIO(file.getvalue())
        ds = pydicom.dcmread(raw)
        shape = ds.pixel_array.shape
        image_2d = ds.pixel_array[0].astype(float) # usually this is a 3d array, so just take the first image slice for now
        image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0
        image_2d_scaled = np.uint8(image_2d_scaled)
        bio = BytesIO()
        w = png.Writer(shape[1], shape[2], greyscale=True)
        w.write(bio, image_2d_scaled)
        return bio
    return file

def pillow_function(content, action):
    im_to_transform=Image.open(content)
    im_transform = None
    # key value pair dictionary of functions
    if action == 'rotate':
        im_transform = im_to_transform.rotate(180)
    elif action == 'crop':
        im_transform = im_to_transform.crop((335, 345, 565, 560))

    return im_transform

def parse_contents(contents, filename, date):
    #data_protected_path = '/Users/jonc101/Desktop/input/'
    #image_obj = Image.open(data_protected_path + filename)
    #rotated_image = image_obj.rotate(180)
    #t = '/Users/jonc101/Documents/Biomedical_Data_Science/assets/data/'
    #name_directory =  t + "test" + ".png"
    #rotated_image.save(name_directory)

    return html.Div([
        html.H5(filename),
        #html.H6(datetime.datetime.fromtimestamp(date)),
        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        # print(type(contents))
        html.Img(src=contents),
        html.Hr(),
        #html.Img(src = app.get_asset_url("data/test.png")),
        #html.Div('Raw Content'),
        #html.Pre(contents[0:200] + '...', style={
        #    'whiteSpace': 'pre-wrap',
        #    'wordBreak': 'break-all'
        #})
    ])


'''
@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents')],
              [State('upload-image', 'filename'),
               State('upload-image', 'last_modified')])
'''

def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        im = []
        for i in list_of_contents:
            im_to_rotate=Image.open(BytesIO(base64.b64decode(i.split(',')[1])))
            im_rotate=im_to_rotate.rotate(180)
            buffered = BytesIO()
            im_rotate.save(buffered, format="png")
                #encoded = base64.b64encode(buff.getvalue()).decode("utf-8")

            im.append('data:image/png;base64,{}'.format(base64.b64encode(buffered.getvalue()).decode("utf-8")))
        #print(im)
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(im, list_of_names, list_of_dates)]
        return children

@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])

def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


page_2_layout =  html.Div([
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
#        html.Button(
#            'Run Operation',
#            id='button-run-operation',
#            style={'margin-right': '10px', 'margin-top': '5px'}
#        ),
        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
            dcc.Tab(label='Image', value='tab-1-example'),
            dcc.Tab(label='Processed Image', value='tab-2-example'),
    #        dcc.Tab(label='Processed Tables', value='tab-3-example'),
        ]),

        html.Div(id='tabs-content-example'),
    #dcc.Link('Go back to home', href='/')
])
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
