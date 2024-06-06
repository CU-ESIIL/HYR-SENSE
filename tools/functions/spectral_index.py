# spectral_index.py

def normalized_diff(input_xarray, band1=650, band2=850):
    """
    This function takes an input orthorectified EMIT xarray image and calculates a normalized-difference spectral index 
    image based on the selected bands. The assumption is the input image is an EMIT image in xarray format 
    prepared using the emit_xarray() function from emit_tools.

    The function provided in the traditional two-band normalized difference index format, i.e.  NDI = Band2-Band1 / Band2+Band1

    Function parameters:
    param: input_xarray is the input EMIT xarray image currently located in memory; at present this will not accept 
    the full path to a file that hasn't been loaded into memory yet (TODO)
    
    param: band1 the EMIT band number to use for band 1
    
    param: band2 the EMIT band number to use for band 2
    """
    
    reflb1 = input_xarray.sel(wavelengths=band1, method='nearest')
    reflb2 = input_xarray.sel(wavelengths=band2, method='nearest')
    ndiff_image = (reflb2-reflb1)/(reflb2+reflb1)
    
    return(ndiff_image)


def pri2(input_xarray, band1=531, band2=570):
    """
    This function takes an input orthorectified EMIT xarray image and calculates a Photochemical Reflectance Index (PRI)
    image based on the selected bands. This function outputs the PRI2, which is the PRI scaled on a 0-1 scale
    for simpler interpretation of the variation in PRI.The assumption is the input image is an EMIT image in xarray 
    format prepared using the emit_xarray() function from emit_tools.

    Function parameters:
    param: input_xarray is the input EMIT xarray image currently located in memory; at present this will not accept 
    the full path to a file that hasn't been loaded into memory yet (TODO)
    
    param: band1 the EMIT band number to use for band 1
    
    param: band2 the EMIT band number to use for band 2
    """
    
    reflb1 = input_xarray.sel(wavelengths=band1, method='nearest')
    reflb2 = input_xarray.sel(wavelengths=band2, method='nearest')
    pri = (reflb1-reflb2)/(reflb1+reflb2)
    pri2_output = (pri+1)/2
    return(pri2_output)


