import os,sys
work_dir=sys.argv[0].find('/')
if (work_dir>-1):
  work_dir=sys.argv[0].rindex('/')
  work_dir=sys.argv[0][0:work_dir]
else:
  work_dir='.'
os.chdir(work_dir)
execfile('init.py')

if (len(sys.argv)<2):
  print 'expecting at least 3 file names'       

band_cal=[]
for bp in sys.argv[2:(len(sys.argv)-1)]:
  if os.path.isdir(bp):
    band_cal.append(bp)
  else:
    print 'no file: '+bp

bp_time={}
for bp in band_cal:
   cmd='%s/prthd in=%s\n'%(env['MIRBIN'],bp)
   rt=subprocess.check_output(cmd.split(' '))
   n=rt.find('First time')
   bp_time[rt[(n+12):(n+30)]]=bp

bp_l=bp_time.keys()
bp_l.sort()
band_cal=[]
for n in range(len(bp_l)):
  band_cal.append(bp_time[bp_l[n]])




cmd='/usr/local/miriad/linux64/bin/uvcat vis=%s out=%s\n'  %(','.join(band_cal),sys.argv[-1])
print cmd
os.system(cmd)

cmd='%s/pgflag "command=<be" options=nodis vis=%s\n'%(env['MIRBIN'], sys.argv[-1])
print cmd
os.system(cmd)

cmd='/usr/local/miriad/linux64/bin/mfcal interval=5 options=interpolate vis=%s\n'  %(sys.argv[-1])
print cmd
os.system(cmd)
cmd='/usr/local/miriad/linux64/bin/gpcal interval=0.1 options=xyvary vis=%s\n'  %(sys.argv[-1])
print cmd
os.system(cmd)
#time.sleep(5)
