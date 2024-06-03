# spectral_index.py

def normalized_diff(input_xarray = ds_geo, band1=650, band2=850):
    """
    This function takes an input xarray image and calculates a NDVI image based on the selected bands.  
    The assumption is the input image is an EMIT image in xarray format prepared using the emit_xarray() 
    function from emit_tools

    The function format is Band2-Band1 / Band2+Band1

    param: input_xarray is the input EMIT xarray in memory
    param: band1 the EMIT band number to use for band 1
    param: band3 the EMIT band number to use for band 3
    """
    
    reflb1 = input_xarray.sel(wavelengths=band1, method='nearest')
    reflb2 = input_xarray.sel(wavelengths=band2, method='nearest')
    ndiff_image = (reflb2-reflb1)/(reflb2+reflb1)
    
    return(ndiff_image)