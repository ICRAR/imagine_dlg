import os,sys
work_dir=sys.argv[0].find('/')
if (work_dir>-1):
  work_dir=sys.argv[0].rindex('/')
  work_dir=sys.argv[0][0:work_dir]
else:
  work_dir='.'
os.chdir(work_dir)
execfile('init.py')

if (len(sys.argv)<4):
  print 'expecting 3 file names'       

os.system('rm -r %s'%(sys.argv[3]))
# Adding option mosaic works for target, but not for BPass
cmd='TMPDIR=/tmp %s/invert stokes=i vis=%s map=%s robust=-2 cell=1 options=mfs,mosaic\n'%(env['MIRBIN'],sys.argv[2],sys.argv[3])
print cmd
os.system(cmd)
