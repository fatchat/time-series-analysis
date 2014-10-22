
# coding: utf-8

# In[1]:

from bs4 import BeautifulSoup
import datetime
import os


# In[2]:

def get_ds_index(datasources):
    for idx,ds in enumerate(datasources):
        if ds.type and ds.type.contents[0].strip()==u'GAUGE':
            return idx


# In[3]:

def get_values(rras,ds_index):
    timeseries=[]
    valueseries=[]
    for rra in rras:
        cf=rra.cf.contents[0].strip()
        pdp_per_row=int(rra.pdp_per_row.contents[0])
        if cf=='AVERAGE' and pdp_per_row==1:
            rows=rra.database.findAll('row')
            for row in rows:
                epoch_time = int(row.previous_sibling.previous_sibling.split('/')[1])
                dt=datetime.datetime.fromtimestamp(epoch_time)
                value=float(row.v.contents[ds_index])
                timeseries.append(dt)
                valueseries.append(value)
    return (timeseries, valueseries)


# In[4]:

def load_data(filename):
    inputfile = open(filename, "r")
    soup=BeautifulSoup(inputfile.read())
    ds_index=get_ds_index(soup.rrd.findAll('ds'))
    return get_values(soup.rrd.findAll('rra'),ds_index)


# In[5]:

def process_rrd_xmls(base_dir,xmlfiles):
    for ent in os.listdir(base_dir):
        entry='%s\\%s' % (base_dir, ent)
        if os.path.isdir(entry):
            process_rrd_xmls(entry,xmlfiles)
        elif entry.endswith('.xml'):
            xmlfiles.append(entry)


# In[6]:

xmlfiles=[]
process_rrd_xmls(r'f:\time series data',xmlfiles)


# In[7]:

for ifile in xmlfiles:
    (time_series,value_series)=load_data(ifile)
    print('%d points from %s to %s' % (len(value_series), time_series[0].strftime('%Y-%m-%d %H:%M:%S'), time_series[-1].strftime('%Y-%m-%d %H:%M:%S')))


# In[ ]:



