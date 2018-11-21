import os
import geopandas as gpd


from utils.filtering import (drop_bad_geometries,
                             filter_faults_inside_other_dataset,
                             filter_faults_crossing_other_faults)


master_df = gpd.read_file('../outputs/geojson/gem_active_faults.geojson')
mdf_write_path = '../outputs/geojson/gem_active_faults_harmonized.geojson'
mdf_write_path_gpkg = '../outputs/geopackage/gem_active_faults_harmonized.gpkg'
mdf_write_path_shp = '../outputs/shapefile/gem_active_faults_harmonized.shp'

mdf = master_df.copy(deep=True)
n_faults_init = len(mdf)

print('Dropping faults with bad geometries...')
mdf = drop_bad_geometries(mdf, verbose=True)

print('Filtering SHARE faults with EMME overlap...')
mdf = filter_faults_inside_other_dataset(mdf, 'SHARE', 'EMME')

print('Filtering SHARE faults with N_Africa overlap...')
mdf = filter_faults_inside_other_dataset(mdf, 'SHARE', 'GEM_N_Africa',
                                         inside_type='intersects')

#print('Filtering Thailand faults that cross Myanmar faults...')
#mdf = filter_faults_crossing_other_faults(mdf, 'thailand', 'myanmar')

#print('Filtering HimatTibetMap faults that cross Myanmar faults...')
#mdf = filter_faults_crossing_other_faults(mdf, 'HimaTibetMap', 'myanmar')

print('Filtering HimatTibetMap faults that cross EMME faults...')
mdf = filter_faults_crossing_other_faults(mdf, 'HimaTibetMap', 'EMME')

print('Filtering HimatTibetMap faults that cross NE Asia faults...')
mdf = filter_faults_crossing_other_faults(mdf, 'HimaTibetMap', 'GEM_NE_Asia')

print('Filtering HimatTibetMap faults that cross SE Asia faults...')
mdf = filter_faults_crossing_other_faults(mdf, 'HimaTibetMap', 'EOS_SE_Asia')

#print('Filtering Thailand faults that cross HimatTibetMap faults...')
#mdf = filter_faults_crossing_other_faults(mdf, 'thailand', 'HimaTibetMap')

print('Filtering Bird faults that cross SHARE faults...')
mdf = filter_faults_crossing_other_faults(mdf, 'Bird 2003', 'SHARE')

#print('Filtering Bird faults that cross SE Asia faults...')
#mdf = filter_faults_crossing_other_faults(mdf, 'Bird 2003', 'EOS_SE_Asia')

print('Filtering Bird faults with CCARA overlap...')
mdf = filter_faults_inside_other_dataset(mdf, 'Bird 2003',
                                         'GEM_Central_Am_Carib',
                                         inside_type='intersects')

print('Filtering Bird faults with ATA overlap...')
mdf = filter_faults_inside_other_dataset(mdf, 'Bird 2003',
                                         'Active Tectonics of the Andes',
                                         inside_type='intersects')

#print('Filtering Bird faults that cross ATA faults...')
#mdf = filter_faults_crossing_other_faults(mdf, 'Bird 2003',
#                                          'Active Tectonics of the Andes')

print('Filtering Bird faults with SARA overlap...')
mdf = filter_faults_inside_other_dataset(mdf, 'Bird 2003', 'SARA',
                                         inside_type='intersects')

print('Filtering Bird faults with EMME overlap...')
mdf = filter_faults_inside_other_dataset(mdf, 'Bird 2003', 'EMME',
                                         inside_type='intersects')

print('Filtering ATA faults that cross SARA faults...')
mdf = filter_faults_crossing_other_faults(mdf, 'Active Tectonics of the Andes',
                                          'SARA')

print('Filtering US faults that cross Mexico...')
mdf = filter_faults_crossing_other_faults(mdf, 'USGS Hazfaults 2014', 
                                          'Villegas Mexico')

print('Filtering Africa faults with EMME overlap...')
mdf = filter_faults_inside_other_dataset(mdf, 'Macgregor_AfricaFaults', 'EMME',
                                         inside_type='intersects')

print('Filtering Africa faults with SHARE overlap...')
mdf = filter_faults_inside_other_dataset(mdf, 'Macgregor_AfricaFaults', 
                                         'SHARE',
                                         inside_type='intersects')

print('Filtering EOS faults that cross Phil faults')
mdf = filter_faults_crossing_other_faults(mdf, 'EOS_SE_Asia',
                                          'philippines')

print('Filtering Bird faults that cross EOS faults')
mdf = filter_faults_crossing_other_faults(mdf, 'Bird 2003', 'EOS_SE_Asia')

n_faults_final = len(mdf)
n_faults_removed = n_faults_init - n_faults_final

print('Done filtering.\n{} initial faults.\n'.format(n_faults_init) +
      'Removed {} faults.\n{} final faults.'.format(n_faults_removed,
                                                    n_faults_final))

try:
    os.remove(mdf_write_path)
except:
    pass

print('writing output files')

print('writing geojson')
mdf.to_file(mdf_write_path, driver='GeoJSON')

print('writing geopackage')
try:
    mdf.to_file(mdf_write_path_gpkg, driver='GPKG')
except Exception as e:
    print(e)

print('writing shapefile')
try:
    mdf.to_file(mdf_write_path_shp)
except Exception as e:
    print(e)
