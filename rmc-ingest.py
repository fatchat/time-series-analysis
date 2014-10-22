from bs4 import BeautifulSoup
import datetime
import os
import shutil
import zipfile
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--base-dir', required=True)
args=parser.parse_args()

def get_ds_index(datasources):
    for idx,ds in enumerate(datasources):
        if ds.type and ds.type.contents[0].strip()==u'GAUGE':
            return idx

def send_values(rras,ds_index):
    for rra in rras:
        cf=rra.cf.contents[0].strip()
        pdp_per_row=int(rra.pdp_per_row.contents[0])
        if cf=='AVERAGE' and pdp_per_row==1:
            rows=rra.database.findAll('row')
            for row in rows:
                epoch_time = int(row.previous_sibling.previous_sibling.split('/')[1])
                dt=datetime.datetime.fromtimestamp(epoch_time)
                value=float(row.v.contents[ds_index])
                print('send packet     t=%s     v=%f' % (dt.strftime('%Y-%m-%d %H:%M:%S'), value))

def send_data(filename):
    inputfile = open(filename, "r")
    soup=BeautifulSoup(inputfile.read())
    ds_index=get_ds_index(soup.rrd.findAll('ds'))
    send_values(soup.rrd.findAll('rra'),ds_index)

def get_rrd_xmls(base_dir):
    for ent in os.listdir(base_dir):
        entry='%s\\%s' % (base_dir, ent)
        if os.path.isdir(entry):
            get_rrd_xmls(entry)
        elif entry.endswith('.xml'):
            print(entry)
            send_data(entry)

def get_rrd_xmls_from_zipfiles(base_dir):
    tempdir=base_dir+r'\.temp-extraction-point'

    if os.path.exists(tempdir):
        shutil.rmtree(tempdir)
    os.mkdir(tempdir)

    for ent in os.listdir(base_dir):
        if ent.endswith('.zip'):
            entry=base_dir+'\\'+ent
            print('processing %s' % entry)
            zf=zipfile.ZipFile(entry)
            zf.extractall(tempdir)
            get_rrd_xmls(tempdir)
            shutil.rmtree(tempdir)
            os.mkdir(tempdir)

    shutil.rmtree(tempdir)

# -- start
#get_rrd_xmls(args.base_dir)
get_rrd_xmls_from_zipfiles(args.base_dir)
