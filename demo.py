"""
demo.py
Spring 2022 PJW

Demonstrate types of joins and handling of duplicate data. Also show
use of pd.to_datetime().
"""

import pandas as pd

#
#  Read data about property parcels
#

parcels = pd.read_csv('parcels.csv',dtype=str)
print( len(parcels) )
print( parcels )

#%%
#
#  Check for duplicate tax ids
#

dups = parcels.duplicated( subset='TAX_ID', keep=False )

print( dups )

#
#  How many? Summing a boolean variable adds up the True values
#

print( '\nduplicate parcels:', dups.sum() ) 

#%%
#
#  Read the file of flood zone information
#

flood = pd.read_csv('flood.csv',dtype=str)
flood = flood.sort_values('TAX_ID')

print( len(flood) )
print( flood )

#%%
#
#  Duplicates?
#

dups = flood.duplicated( subset='TAX_ID', keep=False )
print( '\nduplicate flood records:', dups.sum() ) 

dup_rec = flood[ dups ]
print( dup_rec.sort_values('TAX_ID') )

#%%
#
#  Drop all but the first of the duplicated records
#

flood = flood.drop_duplicates( subset='TAX_ID' )

#
#  Find and print the records that have had their duplicates removed
#

fixed = flood['TAX_ID'].isin( dup_rec['TAX_ID'] )
print( flood[ fixed ] )

dups = flood.duplicated( subset='TAX_ID', keep=False )
print( '\nduplicate flood records:', dups.sum() ) 

#%%
#
#  Outer: keeps all records in both datasets
#

join_o = parcels.merge(flood,
                      on="TAX_ID", 
                      how='outer', 
                      validate='1:1', 
                      indicator=True)

print( '\nOuter records:', len(join_o) )
print( '\nOuter:\n', join_o['_merge'].value_counts(), sep='' )

#%%
#
#  Inner: only records in both
#

join_i = parcels.merge(flood,
                      on="TAX_ID", 
                      how='inner', 
                      validate='1:1', 
                      indicator=True)

print( len(join_i) )

print( '\nInner records:', len(join_i) )
print( '\nOuter:\n', join_o['_merge'].value_counts(), sep='' )
print( '\nInner:\n', join_i['_merge'].value_counts(), sep='' )

#%%
#
#  Left: keep all records in the left dataset
#

join_l = parcels.merge(flood,
                      on="TAX_ID", 
                      how='left', 
                      validate='1:1', 
                      indicator=True)

print( len(join_l) )

print( '\nLeft records:', len(join_l) )
print( '\nOuter:\n', join_o['_merge'].value_counts(), sep='' )
print( '\nLeft:\n', join_l['_merge'].value_counts(), sep='' )

#%%
#
#  Right: keep all records in the right dataset
#

join_r = parcels.merge(flood,
                      on="TAX_ID", 
                      how='right', 
                      validate='1:1', 
                      indicator=True)

print( len(join_r) )

print( '\nRight records:', len(join_r) )
print( '\nOuter:\n', join_o['_merge'].value_counts(), sep='' )
print( '\nRight:\n', join_r['_merge'].value_counts(), sep='' )

#%%
#
#  Default: does inner if how isn't given
#

join_d = parcels.merge(flood, 
                      on="TAX_ID", 
                      validate='1:1', 
                      indicator=True)

print( len(join_d) )

print( '\nDefault records:', len(join_d) )
print( '\nInner:\n', join_i['_merge'].value_counts(), sep='' )
print( '\nDefault:\n', join_d['_merge'].value_counts(), sep='' )

#%%
#
#  Now show the use of pd.to_datetime()
#

recs = pd.read_csv('date.csv')

date = pd.to_datetime(recs['ts'])

recs['date'] = date
recs['day'] = date.dt.day
recs['hour'] = date.dt.hour

print( recs )
