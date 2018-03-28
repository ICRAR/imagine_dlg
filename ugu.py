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

tmp_file=sys.argv[-3]+'.cont'
#os.system('rm -r '+tmp_file)
os.system('rm -r '+' '.join([tmp_file,sys.argv[-1]]))

tgt_list=[]
for tg in sys.argv[2:(len(sys.argv)-2)]:
  if os.path.isdir(tg):
    tgt_list.append(tg)
  else:
    print 'no file: '+tg

tg_time={}
for tg in tgt_list:
   cmd='%s/prthd in=%s\n'%(env['MIRBIN'],tg)
   rt=subprocess.check_output(cmd.split(' '))
   n=rt.find('First time')
   tg_time[rt[(n+12):(n+30)]]=tg

tg_l=tg_time.keys()
tg_l.sort()
tgt_list=[]
for n in range(len(tg_l)):
  tgt_list.append(tg_time[tg_l[n]])


cmd='%s/uvcat vis=%s out=%s\n'  %(env['MIRBIN'],','.join(tgt_list),tmp_file)
print cmd
os.system(cmd)
cmd='%s/gpcopy vis=%s out=%s\n'%(env['MIRBIN'], sys.argv[-2], tmp_file)
print cmd
os.system(cmd)
cmd='%s/pgflag "command=<be" options=nodis vis=%s\n'%(env['MIRBIN'], tmp_file)
print cmd
os.system(cmd)

## Estimate 7Jy noise per channel (SEFD=400, chan=0.5kHz tint=10)
#cmd='%s/uvflag "select=amp(40)" flagval=flag vis=%s\n'%(env['MIRBIN'],tmp_file)
#print cmd
#os.system(cmd)

if os.path.isdir(sys.argv[-1]):
 sys.argv[-1]=sys.argv[-1]+'.line'

line='velo,%d,%.2f,%.2f'%((line_vmax-line_vmin)/width,line_vmin,width)
cmd='MIRCAT=%s %s/uvlin vis=%s out=%s\n'%(env['MIRCAT'], env['MIRBIN'], tmp_file, sys.argv[-1])
print cmd+' SOME CHANNEL SELECTION?'
os.system(cmd)
