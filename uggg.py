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
  print 'expecting 3 file names'       

phase_cal=[]
for pc in sys.argv[2:(len(sys.argv)-2)]:
  if os.path.isdir(pc):
    phase_cal.append(pc)
  else:
    print 'no file: '+pc

pb_time={}
for pc in phase_cal:
   cmd='%s/prthd in=%s\n'%(env['MIRBIN'],pc)
   rt=subprocess.check_output(cmd.split(' '))
   n=rt.find('First time')
   pb_time[rt[(n+12):(n+30)]]=pc

pb_l=pb_time.keys()
pb_l.sort()
phase_cal=[]
for n in range(len(pb_l)):
  phase_cal.append(pb_time[pb_l[n]])



cmd='%s/uvcat vis=%s out=%s\n'  %(env['MIRBIN'],','.join(phase_cal),sys.argv[-1])
print cmd
os.system(cmd)
cmd='%s/gpcopy vis=%s out=%s\n'%(env['MIRBIN'], sys.argv[-2], sys.argv[-1])
print cmd
os.system(cmd)
cmd='%s/gpcal options=nopol vis=%s \n'%(env['MIRBIN'], sys.argv[-1])
print cmd
os.system(cmd)
cmd='%s/gpboot cal=%s vis=%s\n'%(env['MIRBIN'], sys.argv[-2], sys.argv[-1])
print cmd
os.system(cmd)
cmd='%s/pgflag "command=<be" options=nodis vis=%s\n'%(env['MIRBIN'], sys.argv[-1])
print cmd
os.system(cmd)

#time.sleep(5)
