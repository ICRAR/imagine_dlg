try:
  files
except NameError:
  import time,sys
  import numpy
  import scipy
  #import matplotlib
  from numpy import *
  #from pylab import *
  from scipy import *
  #import scipy.io.array_import
  import subprocess
  import os
  import sys
  import ast
  import commands
  from read_parameters import read_parameters
  import pre_conditions as pc
  #
  if (len(sys.argv)<1):
    print 'No parameter file given'
    exit()       
  # Quit now
  #
  par = read_parameters(sys.argv[1])
  print 'the parameters are:'
  rest_freq=1.6654081
  print par
  #
  # change naming convention based on archival data if needed:
  # from LVHIS (C1341)
  target_dir_name = par['target']
  if par['target'] == 'j2052-69':
      target_dir_name = 'ic5052'
  # read the pre defined input for the different targets.
  PhaseCal, frequency, alt_freq, vmin, nchan, width, vel, line_vmin, line_vmax= pc.get_input(par['target'],par['project'])
  #
  #frequency=rest_freq*1000*(1-line_vmin/3e5)
  #frequency=int(frequency*10+0.5)/10.0
  #
  # change to the processing directory:
  os.chdir(par['process_dir'])
  #  
  # make the target and comfiguration directory
  os.system('mkdir ' + target_dir_name)
  os.chdir(target_dir_name)
  os.system('mkdir ' + par['configuration'])
  os.chdir(par['configuration'])
  full_data_path=par['process_dir']+'/'+target_dir_name+'/'+par['configuration']+'/'
  #
  # define all the objects
  source = par['target'] + '.' + str(frequency)
  band_cal1 = '1934-638' + '.' + str(frequency)
  band_cal2 = '0823-500' + '.' + str(frequency)
  phase_cal = PhaseCal + '.' + str(frequency)
  #
  # alternative names based on a different frequency
  alt_source = par['target'] + '.' + str(alt_freq)
  alt_band_cal1 = '1934-638' + '.' + str(alt_freq)
  alt_band_cal2 = '0823-500' + '.' + str(alt_freq)
  alt_phase_cal = PhaseCal + '.' + str(alt_freq)
  #
  print 'alternative names'
  print alt_source
  print alt_band_cal1
  print alt_band_cal2
  print alt_phase_cal
  print source
  #
  # define files to be reduced:
  files = par['files']
  files.replace("\n","")
  files = ast.literal_eval(par['files'])
  print files
  #
  # don't remove this directory as it may have sources from a previous run
  #os.system('rm -rf uvlin_files')
  os.system('mkdir uvlin_files')
  #
  # make empty arrays storing the files with calibrators
  band_dir1 = []
  band_dir2 = []
  phase_dir = []
  source_dir = []
  #
  print band_cal1
  print band_cal2
  print phase_cal
  print source
  #
  print str(sys.argv[0])
  #
  import os, subprocess as sp, json
  import datetime
  source = 'source /usr/local/miriad/MIRRC.sh'
  dump = '/usr/bin/python -c "import os, json;print json.dumps(dict(os.environ))"'
  pipe = sp.Popen(['/bin/bash', '-c', '%s && %s' %(source,dump)], stdout=sp.PIPE)
  env = json.loads(pipe.stdout.read())
  os.environ = env
  #
  #fp=open('/tmp/imaging.log-'+datetime.datetime.utcnow().isoformat(),'a')
  #fp.write('Running %s\n\n'%(str(sys.argv)))
  #fp.close()
