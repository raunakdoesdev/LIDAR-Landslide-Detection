"""Operates on data from qtm_extracted_data and cleaned_data to extract relevant features for learning"""

import richdem as rd
import pandas as pd
import pdfplot  # my own personal library for managing figures

landslides = pd.read_pickle('data/cleaned_data/landslides_cleaned.pkl')


def plot(dat, points, title="Temp"):
    fig, ax = rd.rdShow(dat, axes=False, cmap='jet', figsize=(8, 5.5))
    for point in points:
        ax.scatter([point[0]], [point[1]], marker='x', c='black')
        ax.text(point[0] + 30, point[1] + 30, 'Landslide')
    ax.set_title(title)


for i, landslide in landslides.iterrows():
    dem = rd.LoadGDAL(landslide['DTM Path'])
    plot(dem, landslide['Landslides'], title=f'DEM for {landslide["DTM Path"]}')
    slope = rd.TerrainAttribute(dem, attrib='slope_riserun')
    plot(slope, landslide['Landslides'], title=f'Slope for {landslide["DTM Path"]}')
    aspect = rd.TerrainAttribute(dem, attrib='aspect')
    plot(aspect, landslide['Landslides'], title=f'Aspect for {landslide["DTM Path"]}')
    profile_curvature = rd.TerrainAttribute(dem, attrib='profile_curvature')
    plot(profile_curvature, landslide['Landslides'], title=f'Profile Curvature for {landslide["DTM Path"]}')
    planform_curvature = rd.TerrainAttribute(dem, attrib='planform_curvature')
    plot(planform_curvature, landslide['Landslides'], title=f'Planform Curvature for {landslide["DTM Path"]}')
    curvature = rd.TerrainAttribute(dem, attrib='curvature')
    plot(curvature, landslide['Landslides'], title=f'Curvature for {landslide["DTM Path"]}')
pdfplot.save_figs(folder='figures')
