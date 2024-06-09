# spectral_index.py

# load dependencies
import rasterio as rio

def normalized_diff(input_xarray, band1=650, band2=850, index_name="ndvi", proj="EPSG:4326"):
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
    
    param: index_name name to give the new data variable, e.g. default is "ndvi"

    param: proj EPSG projection code to set the coordinate reference system of the output image. Default is "EPSG:4326"
    """

    # calculate the index
    reflb1 = input_xarray.sel(wavelengths=band1, method='nearest')
    reflb2 = input_xarray.sel(wavelengths=band2, method='nearest')
    ndiff_image = (reflb2-reflb1)/(reflb2+reflb1)

    # rename the output variable
    ndiff_image[index_name] = ndiff_image['reflectance']
    ndiff_image = ndiff_image.drop(['reflectance'])

    # set the CRS
    ndiff_image = ndiff_image.rio.write_crs(proj) # Set the CRS

    # Remove additional coordinates that are not relevant
    ndiff_image = ndiff_image.drop_vars(['wavelengths', 'fwhm', 'good_wavelengths', 'elev'], errors='ignore')

    return(ndiff_image.squeeze())


def pri(input_xarray, band1=531, band2=570, scaled=True, index_name="pri", proj="EPSG:4326"):
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

    param: scaled scale the output pri
    
    param: index_name name to give the new data variable, e.g. default is "pri"

    param: proj EPSG projection code to set the coordinate reference system of the output image. Default is "EPSG:4326"
    """
    
    reflb1 = input_xarray.sel(wavelengths=band1, method='nearest')
    reflb2 = input_xarray.sel(wavelengths=band2, method='nearest')
    pri = (reflb1-reflb2)/(reflb1+reflb2)

    if scaled == True:
        pri = (pri+1)/2

    # rename the output variable
    pri[index_name] = pri['reflectance']
    pri = pri.drop(['reflectance'])

    # set the CRS
    pri = pri.rio.write_crs(proj) # Set the CRS

    # Remove additional coordinates that are not relevant
    pri = pri.drop_vars(['wavelengths', 'fwhm', 'good_wavelengths', 'elev'], errors='ignore')

    return(pri.squeeze())


def simple_ratio(input_xarray, band1=900, band2=970, index_name="wbi", proj="EPSG:4326"):
    """
    This function takes an input orthorectified EMIT xarray image and calculates a simple ration index image based on
    the selected bands. The assumption is the input image is an EMIT image in xarray 
    format prepared using the emit_xarray() function from emit_tools.

    Function parameters:
    param: input_xarray is the input EMIT xarray image currently located in memory; at present this will not accept 
    the full path to a file that hasn't been loaded into memory yet (TODO)
    
    param: band1 the EMIT band number to use for band 1
    
    param: band2 the EMIT band number to use for band 2
    """
    
    reflb1 = input_xarray.sel(wavelengths=band1, method='nearest')
    reflb2 = input_xarray.sel(wavelengths=band2, method='nearest')
    sr = reflb1/reflb2

    # rename the output variable
    sr[index_name] = sr['reflectance']
    sr = sr.drop(['reflectance'])

    # set the CRS
    sr = sr.rio.write_crs(proj) # Set the CRS

    # Remove additional coordinates that are not relevant
    sr = sr.drop_vars(['wavelengths', 'fwhm', 'good_wavelengths', 'elev'], errors='ignore')

    return(sr.squeeze())







    