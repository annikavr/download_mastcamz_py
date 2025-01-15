import re
import os
import requests

# Define the base URL for the PDS Imaging Node API
# base_url = 'https://pds-imaging.jpl.nasa.gov/api/search/'
# Example list of image IDs (you can replace this with actual API responses)
image_ids = [
    'ZLF_0089_0674855109_239RAD_N0040048ZCAM08050_034085J03.png',
    'ZLF_0089_0674855109_239RAD_N0040048ZCAM08050_034085J03.png',
    'ZLF_0089_0674855109_239RAD_N0040048ZCAM07050_034085J03.png'
]

# Define the regex pattern for matching image IDs
pattern = r'Z(L|R)\d+_\d+_\d+RAD_N\d+ZCAM(07|08|09)\d+_\d+LM\d+\.png'

# Create a dictionary to hold ZCAM groupings
zcam_groups = {}

# Process each image ID
for image_id in image_ids:
    if re.match(pattern, image_id):
        # Extract the ZCAM group (e.g., ZCAM08050, ZCAM07050, etc.)
        zcam_group = re.search(r'ZCAM(07|08|09)\d+', image_id).group(0)

        # Add the image ID to the respective ZCAM group
        if zcam_group not in zcam_groups:
            zcam_groups[zcam_group] = []
        zcam_groups[zcam_group].append(image_id)

# Now we fetch the URLs from the API response for each image ID
base_url = 'https://pds-imaging.jpl.nasa.gov/api/search/'
params = {
    'instrument': 'Mastcam-Z',
    'product_type': 'science_calibrated',
    'processing_level': 'radiance_corrected',
    'file_extension': 'png',
    'sequence_id': '08*'
}

# Make the API request
response = requests.get(base_url, params=params)
response.raise_for_status()  # Raise an error for bad status codes

# Parse the JSON response
data = response.json()

# Directory to save the downloaded images
output_dir = 'mastcamz_images'
os.makedirs(output_dir, exist_ok=True)

# Download and save images, grouped by ZCAM group
for zcam_group, images in zcam_groups.items():
    # Create a folder for each ZCAM group
    zcam_folder = os.path.join(output_dir, zcam_group)
    os.makedirs(zcam_folder, exist_ok=True)

    # Check the API response for each image and download it
    for image_id in images:
        # Find the matching image URL in the API response
        for item in data['items']:
            if image_id in item['filename']:  # Matching image ID
                image_url = item['url']  # Extract the URL from the API response
                
                # Download the image
                img_response = requests.get(image_url)
                img_response.raise_for_status()

                # Save the image
                image_path = os.path.join(zcam_folder, image_id)
                with open(image_path, 'wb') as img_file:
                    img_file.write(img_response.content)

                print(f"Downloaded {image_id} to {zcam_folder}")
                break
