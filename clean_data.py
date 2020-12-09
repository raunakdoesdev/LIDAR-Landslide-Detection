"""
This script operates on data from the qtm_extracted_data folder and populates the cleaned_data folder.

The objective of the script is to take the data from geographical format to a more simplified image based numerical format.
"""

import os
import pandas as pd
import gdal
from affine import Affine

landslides = pd.read_csv('data/qtm_extracted_data/landslides.csv', header=0)
landslides['DTM Path'] = [f'data/qtm_extracted_data/{name[-2]}.tif' for name in landslides['Name']]  # path to tif file

pixels = []
for i, row in landslides.iterrows():
    ds = gdal.Open(row['DTM Path'])
    reverse = ~Affine.from_gdal(*ds.GetGeoTransform())
    coord = reverse * (row['X'], row['Y'])
    pixels.append((round(coord[0]), round(coord[1])))

landslides['X'] = [pixel[0] for pixel in pixels]
landslides['Y'] = [pixel[1] for pixel in pixels]

points = []
for tif in landslides['DTM Path'].unique():
    tif_landslides = landslides[landslides['DTM Path'] == tif]
    points.append(list(zip(tif_landslides['X'], tif_landslides['Y'])))

clean_df = pd.DataFrame({'DTM Path': landslides['DTM Path'].unique(), 'Landslides': points},
                        columns=['DTM Path', 'Landslides'])
clean_df.to_pickle('data/cleaned_data/landslides_cleaned.pkl')
# landslides[['Name', 'X', 'Y', 'DTM Path']].to_csv('cleaned_data/landslides_cleaned.csv')
