"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/stable/plugins/building_a_plugin/guides.html#sample-data

Replace code below according to your needs.
"""
from __future__ import annotations

from ._reader import reader_function


def load_sample_data(url: str):
    """Generates an image"""
    # Return list of tuples
    # [(data1, add_image_kwargs1), (data2, add_image_kwargs2)]
    # Check the documentation for more information about the
    # add_image_kwargs
    # https://napari.org/stable/api/napari.Viewer.html#napari.Viewer.add_image
    reader_function(url)
    return [(None,),]

def sample_data_drosophila():    
    url = 'https://livingobjects.ebi.ac.uk/bioimaging-integrator-data/S-BIAD3424/drosophila_LSBM.brim.zarr'
    return load_sample_data(url)
def sample_data_zfeye():
    url = 'https://livingobjects.ebi.ac.uk/bioimaging-integrator-data/S-BIAD3424/zebrafish_eye_confocal.brim.zarr'
    return load_sample_data(url)
def sample_data_zfSBS():
    url = 'https://livingobjects.ebi.ac.uk/bioimaging-integrator-data/S-BIAD3424/zebrafish_ECM_SBS.brim.zarr'
    return load_sample_data(url)
def sample_data_beadsFTBM():
    url = 'https://livingobjects.ebi.ac.uk/bioimaging-integrator-data/S-BIAD3424/oil_beads_FTBM.brim.zarr'
    return load_sample_data(url)