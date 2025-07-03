import re  # For regular expression matching
import os  # For creating directories and handling file paths
import requests  # For making HTTP requests to the API

# Define the base URL for the PDS Imaging Node API
base_url = 'https://pds-imaging.jpl.nasa.gov/api/search/'

# Example list of image IDs (replace this with real data from the API or files)
# These should match filenames you want to download
# image_ids = [
#     'ZLF_0089_0674855109_239RAD_N0040048ZCAM08050_034085J03.png',
#     'ZLF_0089_0674855109_239RAD_N0040048ZCAM08050_034085J03.png',
#     'ZLF_0089_0674855109_239RAD_N0040048ZCAM07050_034085J03.png'
# ]

# Define the regex pattern to identify valid ZCAM image filenames
pattern = r'Z(L|R)\d+_\d+_\d+RAD_N\d+ZCAM(07|08|09)\d+_\d+LM\d+\.png'

# Create a dictionary to store image IDs grouped by their ZCAM number
zcam_groups = {}

# Iterate through each image ID in the list
for image_id in image_ids:
    # Check if the image ID matches the defined regex pattern
    if re.match(pattern, image_id):
        # Extract the ZCAM group (e.g., ZCAM07050, ZCAM08050, etc.)
        zcam_group = re.search(r'ZCAM(07|08|09)\d+', image_id).group(0)

        # If this ZCAM group is not in the dictionary yet, add it
        if zcam_group not in zcam_groups:
            zcam_groups[zcam_group] = []

        # Add the current image ID to the appropriate ZCAM group
        zcam_groups[zcam_group].append(image_id)

# Redefine the base URL for querying the API
base_url = 'https://pds-imaging.jpl.nasa.gov/api/search/'

# Define query parameters for the API request
params = {
    'instrument': 'Mastcam-Z',  # Filter for Mastcam-Z instrument
    'product_type': 'science_calibrated',  # Only get calibrated science products
    'processing_level': 'radiance_corrected',  # Only get radiance-corrected data
    'file_extension': 'png',  # Only want PNG image files
    'sequence_id': '08*'  # Sequence IDs starting with '08'
}

# Send a GET request to the API using the above parameters
response = requests.get(base_url, params=params)

# Raise an exception if the API call fails (e.g., bad status code)
response.raise_for_status()

# Convert the JSON response from the API to a Python dictionary
data = response.json()

# Define the directory where images will be downloaded and saved
output_dir = 'mastcamz_images'

# Create the output directory if it doesn't already exist
os.makedirs(output_dir, exist_ok=True)

# Iterate through each ZCAM group and its associated image IDs
for zcam_group, images in zcam_groups.items():
    # Create a subfolder for this specific ZCAM group
    zcam_folder = os.path.join(output_dir, zcam_group)
    os.makedirs(zcam_folder, exist_ok=True)

    # Go through each image in this group
    for image_id in images:
        # Loop through all items in the API response to find a matching image
        for item in data['items']:
            # If the image ID is part of the filename, it's a match
            if image_id in item['filename']:
                # Get the image's download URL from the API response
                image_url = item['url']
                
                # Send a GET request to download the image
                img_response = requests.get(image_url)
                img_response.raise_for_status()

                # Define the full path for saving the downloaded image
                image_path = os.path.join(zcam_folder, image_id)

                # Write the image content to a local file
                with open(image_path, 'wb') as img_file:
                    img_file.write(img_response.content)

                # Print a message indicating the image was downloaded successfully
                print(f"Downloaded {image_id} to {zcam_folder}")

                # Stop searching once the image is found and downloaded
                break
