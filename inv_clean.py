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
  print 'expecting at least 3 file names'       
width=0.1
line='velo,%d,%.2f,%.2f'%((line_vmax-line_vmin)/width,line_vmin,width)

cmd='TMPDIR=/tmp %s/invert vis=%s.cont map=%s.icont robust=0 imsize=256 cell=20 stokes=i slop=0.5 "select=-ant(6)" options=mosaic,mfs\n'%(env['MIRBIN'], sys.argv[2].replace('.line',''), sys.argv[3])
print cmd
os.system(cmd)

cmd='TMPDIR=/tmp %s/invert vis=%s map=%s.i beam=%s.beam line=%s robust=0 imsize=256 cell=20 stokes=i slop=0.5 "select=-ant(6)" options=mosaic\n'%(env['MIRBIN'], sys.argv[2], sys.argv[3], sys.argv[3], line)
print cmd
os.system(cmd)
cmd='%s/clean map=%s.i beam=%s.beam out=%s.imodel niters=500 gain=0.5\n'%(env['MIRBIN'],sys.argv[3], sys.argv[3], sys.argv[3])
print cmd
os.system(cmd)
cmd='%s/restor map=%s.i beam=%s.beam model=%s.imodel out=%s.icln\n'%(env['MIRBIN'],sys.argv[3], sys.argv[3], sys.argv[3], sys.argv[3])
print cmd
os.system(cmd)
cmd='tar czvf %s %s.*\n'%(sys.argv[3], sys.argv[3])
print cmd
os.system(cmd)

#time.sleep(5)
