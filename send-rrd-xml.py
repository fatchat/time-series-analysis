#!/usr/bin/python

import os
import sys
import argparse
import subprocess
from datetime import datetime
import logging

# command-line arguments can be specified here
parser=argparse.ArgumentParser('Send RRD data from RMC')
parser.add_argument('--for-real', action='store_true')
args=parser.parse_args()

# set up logging
logfilename= <<<<<PUT THE LOGFILE NAME HERE>>>>>
logging.basicConfig(filename=logfilename,level=logging.INFO,format='%(asctime)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')


# @brief Run the rrdtool on a set of RRD files to extract their data as XML
# @param source_dir	Absolute pathname of directory containing the RRD files
# @param dest_dir Absolute pathname of directory where the XML data should be placed
def extract_rrd_data(source_dir, dest_dir):
	logging.info('source=%s' % (source_dir))
	logging.info('dest=%s' % (dest_dir))

	# first ensure that the source folder was specified correctly
	if not os.path.exists(source_dir):
		logging.error('source folder does not exist')
		return

	# if the destination folder exists, fine, otherwise create it
	if os.path.exists(dest_dir):
		logging.info('dest folder %s exists, continuing' % dest_dir)
	else:
		logging.info('creating dest folder %s' % dest_dir)
		try:
			os.mkdirs(dest_dir)
		except:
			# could not create folder - log this but don't die
			logging.error('Failed to create dest folder')
			return

	# run 'rrdtool dump' on each .rrd file in the source folder
	for file_ in os.listdir(source_dir):
		if file_.endswith('.rrd'):

			# absolute pathname of the rrd file
			rrdfile=source_dir+'/'+file_

			# absoluate pathname of the xml file to be created
			xmlfile=dest_dir+'/'+file_.replace('.rrd', '.xml')

			logging.info('> rrdtool dump %s %s' % (rrdfile, xmlfile))

			# run the rrdtool if the --for-real flag was specified. during testing one
			# may omit the flag and just view the logs to ensure correctness of the various filenames
			if args.for_real:
				try:
					subprocess.check_call(['rrdtool','dump',rrdfile,xmlfile])
				except subprocess.CalledProcessError, e:
					# rrdtool failed for some reason. log the exception and try the next rrd file
					logging.error(e)
					continue

# =====================================================================================================================
# @start

# all output folders will have the same timestamp for a single run
run_time=datetime.strftime(datetime.now(), '%Y-%m-%d.%H.%M.%S')
logging.info('START at %s' % run_time)

# rrd extraction
extract_rrd_data(source_dir=<<<<PLEASE SET SOURCE DIR FOR ADOS>>>>,dest_dir='/mnt/zenbackup/RRDfiles/AD/OScounters/ADOS'+run_time)
extract_rrd_data(source_dir='/opt/zenoss/perf/Devices/172.21.2.1/os/filesystems/C',dest_dir='/mnt/zenbackup/RRDfiles/AD/filesystem/C/ADFilesystemC_'+run_time)
extract_rrd_data(source_dir='/opt/zenoss/perf/Devices/172.21.2.1/os/filesystems/D',dest_dir='/mnt/zenbackup/RRDfiles/AD/filesystem/D/ADFilesystemD_'+run_time)
extract_rrd_data(source_dir='/opt/zenoss/perf/Devices/172.21.2.1/os/interfaces/BASP\ Virtual\ Adapter/',dest_dir='/mnt/zenbackup/RRDfiles/AD/interface/BASPVirtualAdapter/ADInterfaces_'+run_time)

# TODO zip and send the XML files to the HTTP endpoint
# http://azure.microsoft.com/en-us/documentation/articles/storage-python-how-to-use-blob-storage/
# from azure.storage import BlobService
# bs=BlobService(account_name='mlairmcdata',account_key='9b/L+y09Hq7Pvmz2gLmBwovnEL2u5S21klT6LuMnm233UHmgtFo75oaJ3ZehQ+bKTqLYZhg3PS0c7YHhoKyaiw==')
# bs.put_block_blob_from_path('rmc','test',r'f:\RMC Data\send-rrd-xml.py')

