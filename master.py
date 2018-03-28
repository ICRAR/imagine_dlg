import os,sys
if ((len(sys.argv)!=2)):
  print 'Usage: /path/master.py PARFILE\n'
  print 'Expect the PAR (and other required files to be in the same directory as the master'
  print 'which is why the full explicit path is required for the script'
  print 'Data is stashed on /lscratch -- so if that is not there (non-pleiadesXX machines) this will fail'

work_dir=sys.argv[0].find('/')
if (work_dir>-1):
  work_dir=sys.argv[0].rindex('/')
  work_dir=sys.argv[0][0:work_dir]
else:
  work_dir='.'
os.chdir(work_dir)
execfile('init.py')

skip=[]
if (len(sys.argv)>2):
   skip=sys.argv[2].split(',')
   skip.sort()
skip.append('0')

scratch='/lscratch/'
lscratch=' /lscratch/'
if (not os.path.isdir(scratch)):
  scratch='/scratch/'
  lscratch=' /scratch/'
op=scratch+lscratch.join(files)
cmd='python %s/%s %s %s\n'%(work_dir,'archive_cp.py',sys.argv[1],op)
print(cmd)
if (skip[0]!='1'):
  os.system(cmd)
else:
   skip.remove(skip[0])


cmd='python %s/%s %s %s %s\n'%(work_dir,'afu.py',sys.argv[1],op,' '.join([full_data_path+'/bp',full_data_path+'/pc',full_data_path+'/tg']))
print(cmd)
if (skip[0]!='2'):
  os.system(cmd)
else:
   skip.remove(skip[0])

cmd='python %s/%s %s %s\n'%(work_dir,'umg.py',sys.argv[1],full_data_path+'/bp')
print(cmd)
if (skip[0]!='3'):
  os.system(cmd)
else:
   skip.remove(skip[0])
cmd='python %s/%s %s %s %s\n'%(work_dir,'inv.py',sys.argv[1],full_data_path+'/bp',full_data_path+'/bp_out')
print(cmd)
if (skip[0]!='4'):
  os.system(cmd)
else:
   skip.remove(skip[0])

cmd='python %s/%s %s %s %s\n'%(work_dir,'uggg.py',sys.argv[1],full_data_path+'/bp',full_data_path+'/pc')
print(cmd)
if (skip[0]!='5'):
  os.system(cmd)
else:
   skip.remove(skip[0])
cmd='python %s/%s %s %s %s\n'%(work_dir,'inv.py',sys.argv[1],full_data_path+'/pc',full_data_path+'/pc_out')
print(cmd)
if (skip[0]!='6'):
  os.system(cmd)
else:
   skip.remove(skip[0])

cmd='python %s/%s %s %s %s %s\n'%(work_dir,'ugu.py',sys.argv[1],full_data_path+'/tg',full_data_path+'/pc',full_data_path+'/tg_cal')
print(cmd)
if (skip[0]!='7'):
  os.system(cmd)
else:
   skip.remove(skip[0])
cmd='python %s/%s %s %s %s\n'%(work_dir,'inv.py',sys.argv[1],full_data_path+'/tg_cal',full_data_path+'/tg_out')
print(cmd)
if (skip[0]!='8'):
  os.system(cmd)
else:
   skip.remove(skip[0])

cmd='python %s/%s %s %s %s\n'%(work_dir,'inv_clean.py',sys.argv[1],full_data_path+'/tg_cal',full_data_path+'/tg_final')
print(cmd)
if (skip[0]!='9'):
  os.system(cmd)
else:
   skip.remove(skip[0])
