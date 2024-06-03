import xarray as xr
import numpy as np

# Pre-Processing
def mask_aqua(ds):
    
    # EMIT Mask Python script for Aquatic Interest
    # Cirrus Mask
    cirrus_mask = xr.where(ds['reflectance'].sel(wavelengths=1380, method='nearest') < 0.1, 1, 0)
    ds.coords['cirrus_mask'] = (('latitude', 'longitude'), cirrus_mask.data)

    # Land Mask
    land_mask = xr.where(ds['reflectance'].sel(wavelengths=1000, method='nearest') < 0.05, 1, 0)
    ds.coords['land_mask'] = (('latitude', 'longitude'), land_mask.data)

    # Cloud Mask (Sanford)
    total = xr.where(ds['reflectance'].sel(wavelengths=450, method='nearest') > 0.28, 1, 0) + \
            xr.where(ds['reflectance'].sel(wavelengths=1250, method='nearest') > 0.46, 1, 0) + \
            xr.where(ds['reflectance'].sel(wavelengths=1380, method='nearest') > 0.22, 1, 0)

    cloud_mask = xr.where(total.data > 2, 1, 0)
    ds.coords['cloud_mask'] = (('latitude', 'longitude'), cloud_mask.data)

    return ds


def glint_corr(ds, method):

    if method == 'swir':
        med = ds.Rrs.loc[:,:,1500:1650].median()
        gc = ds.Rrs - med

    elif method == 'nir':
        med = ds.Rrs.loc[:,:,800:900].median()
        gc = ds.Rrs - med

    else:
        print('Empty Posthoc Method: Select swir or nir posthoc correction')
        return

    return gc


def rho2Rrs(ds):
    return ds.reflectance / np.pi


# Table 5: Water quality subproducts
def chlor_a(ds, algorithm='moses3'):
    
    if algorithm == 'moses3':

        Rrs_665 = ds.Rrs.sel(wavelengths=665, method='nearest')
        Rrs_708 = ds.Rrs.sel(wavelengths=708, method='nearest')
        Rrs_753 = ds.Rrs.sel(wavelengths=753, method='nearest')

        a = 232.329
        b = 23.174
        chl = a * (Rrs_753 * (1/Rrs_665 - 1/Rrs_708)) + b
        
    elif algorithm == 'moses2':
        
        Rrs_665 = ds.Rrs.sel(wavelengths=665, method='nearest')
        Rrs_708 = ds.Rrs.sel(wavelengths=708, method='nearest')
        
        a = 61.324
        b = 37.94
        chl = a * (Rrs_708 / Rrs_665) - b 
        
    return chl


# Table 7: Subproducts for water column environments
def turbidity(ds, algorithm='dogliotii'):

    if algorithm == 'dogliotti':
        band_op1 = ds.Rrs.sel(wavelengths=645, method='nearest')
        band_op2 = ds.Rrs.sel(wavelengths=859, method='nearest')

        At_op1 = 228.1
        Ct_op1 = 3078.9
        At_op2 = 0.1641
        Ct_op2 = 0.2112

        T_op1 = (At_op1*band_op1)/((1-band_op1)/Ct_op1)
        T_op2 = (At_op2*band_op2)/((1-band_op2)/Ct_op2)

        return T_op1, T_op2
    

# Miscellaneous
def tss(ds, algorithm='nechad'):

    if algorithm == 'miller':    
        Rrs_668 = ds.Rrs.sel(wavelengths=668, method='nearest')

        a = 1140.25
        b = 1.91
        TSS = a * Rrs_668 - b
    
    elif algorithm == 'nechad':
        Rrs = ds.Rrs.sel(wavelengths=665, method='nearest')

        a = 355.85
        b = 1.74
        c = 1728

        TSS = b + (a * np.pi * Rrs) / (1 - (np.pi * Rrs) / c)
        
    return TSS

    
def CIcyano(ds, low=665, center=681, high=709):

    refl_low = ds.reflectance.sel(wavelengths=low, method='nearest')
    refl_center = ds.reflectance.sel(wavelengths=center, method='nearest')
    refl_high = ds.reflectance.sel(wavelengths=high, method='nearest')

    SS = (refl_center - refl_low) + ((refl_low - refl_high) * ((center - low) / (high - low)))
    
    counts = (-SS) * (1.0 * (10 ** 8))
    
    return -SS, counts


def avw(ds):
    
    
    return avw


def qwip(ds):
    
    return qwip
