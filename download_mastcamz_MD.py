import requests
import os

# Define the base URL for the PDS Imaging Node API
base_url = 'https://pds-imaging.jpl.nasa.gov/api/search/'

# Define the search parameters
params = {
    'instrument': 'Mastcam-Z',
    'product_type': 'science_calibrated',
    'processing_level': 'radiance_corrected',
    'file_extension': 'png',
    'sequence_id': '08*'  # Assuming '08*' matches sequence IDs starting with '08'
}

# Mastcam image ID: 
# Z(L or R)*_****_{10*'s}_***RAD_N*******ZCAM{07, 08, or 09}###_****LM***.png 
# Anything with the same ZCAM0#### goes in one folder 
# All images under this path in the ATLAS: 
# mars_2020/mars2020_mastcamz_ops_calibrated/mars2020_mastcamz_ops_calibrated/browse/sol/#####/ids/rdr/zcam/(then the image ID goes here)
# For some 5-digit sol # 

# End up with a set of folders labeled by the individual mosaic (as opposed to individual frames)
# E.g., Mastcam -> Z(R or L)*_****(this is the sol, same for all parts of mosaic)_ZCAM0(7/8/9)###


# Make the API request
response = requests.get(base_url, params=params)
response.raise_for_status()  # Raise an error for bad status codes

# Parse the JSON response
data = response.json()

# Directory to save the downloaded images
output_dir = 'mastcamz_images'
os.makedirs(output_dir, exist_ok=True)

# Download each image
for item in data['items']:
    image_url = item['url']
    image_name = os.path.basename(image_url)
    image_path = os.path.join(output_dir, image_name)
    
    # Download the image
    img_response = requests.get(image_url)
    img_response.raise_for_status()
    
    # Save the image to the output directory
    with open(image_path, 'wb') as img_file:
        img_file.write(img_response.content)
    
    print(f'Downloaded {image_name}')
