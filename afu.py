import os,sys
work_dir=sys.argv[0].find('/')
if (work_dir>-1):
  work_dir=sys.argv[0].rindex('/')
  work_dir=sys.argv[0][0:work_dir]
else:
  work_dir='.'
os.chdir(work_dir)
execfile('init.py')

file_list=','.join(sys.argv[2:len(sys.argv)-3])
sub_dir=sys.argv[2].find('/')
if (sub_dir>-1):
  sub_dir=sys.argv[2][(sys.argv[2].rindex('/')+1):len(sys.argv[2])]+'/'
sub_dir=sys.argv[2]+'.dir/'
#sub_dir='./'
data_file=sys.argv[2]+'.atlod'
print file_list

if (os.path.isdir(sub_dir)):
  print sub_dir+' exists'
else:
  os.mkdir(sub_dir)
os.chdir(sub_dir)
os.system('pwd')

os.system('rm -r '+data_file)
cmd='MIRCAT=%s %s/atlod restfreq=%f options=bary,birdie,rfiflag,noauto edge=0 in=%s ifsel=%s out=%s\n'%(env['MIRCAT'],env['MIRBIN'],rest_freq,file_list, par['if'], data_file)
print cmd
os.system(cmd)
for f in file_list.split(','):
  os.system('rm -r '+f)

cmd='%s/uvlist options=spec vis=%s\n'%(env['MIRBIN'],data_file)
rt=subprocess.check_output(cmd.split(' '))
n=rt.find('Start freq')
freq1=float('%.1f'%((1000*float(rt[(n+27):(n+39)]))))
if (abs(1-freq1/(rest_freq*1000.))>0.1):
   print 'Wrong Data! frequency=%f rest_freq=%f \n'%(freq1,rest_freq)
   exit()
## freq1 does not match frequency!!!

cmd='%s/uvflag edge=20 flagval=flag vis=%s\n'%(env['MIRBIN'],data_file)
print cmd
os.system(cmd)
cmd='%s/uvflag "select=amp(100)" flagval=flag vis=%s\n'%(env['MIRBIN'],data_file)
print cmd
os.system(cmd)
cmd='%s/uvflag select="shadow(25)" flagval=flag vis=%s\n'%(env['MIRBIN'],data_file)
print cmd
os.system(cmd)
cmd='%s/tvclip vis=%s clip=6 options=notv commands=diff,clip\n'%(env['MIRBIN'],data_file)
print cmd
#os.system(cmd)

# cmd='%s/uvsplit vis=%s "select=source(%s)" options=mosaic \n'%(env['MIRBIN'],data_file,band_cal1[0:8])
# print cmd
# os.system(cmd)
# cmd='%s/uvsplit vis=%s "select=source(%s)" options=mosaic \n'%(env['MIRBIN'],data_file,band_cal2[0:8])
# print cmd
# os.system(cmd)
# cmd='%s/uvsplit vis=%s "select=source(%s)" options=mosaic \n'%(env['MIRBIN'],data_file,PhaseCal)
# print cmd
# os.system(cmd)
# cmd='%s/uvsplit vis=%s "select=source(%s)" options=mosaic \n'%(env['MIRBIN'],data_file,target_dir_name)
# print cmd
# os.system(cmd)

cmd='%s/uvsplit vis=%s options=mosaic \n'%(env['MIRBIN'],data_file)
print cmd
os.system(cmd)

#time.sleep(5)
#if (band_cal1)
os.chdir('..')
PhaseCal=sub_dir+PhaseCal+'.'+str(frequency)
target_dir_name=sub_dir+target_dir_name+'.'+str(frequency)
#band_cal=sub_dir+'Bpass'+'.'+str(frequency)
band_cal=[]
if (os.path.isdir(sub_dir+band_cal1)):
    band_cal.append(sub_dir+band_cal1)
elif (os.path.isdir(sub_dir+band_cal2)):
    band_cal.append(sub_dir+band_cal2)

if (len(band_cal)):
    cmd='%s/uvcat vis=%s out=%s\n'%(env['MIRBIN'],','.join(band_cal),sys.argv[-3])
else:
    cmd='echo not making '+sys.argv[-3]
print cmd
os.system(cmd)

phase_cal=[]
if (os.path.isdir(PhaseCal)):
    phase_cal.append(PhaseCal)

if (len(phase_cal)):
    cmd='%s/uvcat vis=%s out=%s\n'%(env['MIRBIN'],','.join(phase_cal),sys.argv[-2])
else:
    cmd='echo not making '+sys.argv[-2]
print cmd
os.system(cmd)

target_list=[]
if (os.path.isdir(target_dir_name)):
    target_list.append(target_dir_name)
else: ## Occasionally pnt is used as the name
    if (os.path.isdir(sub_dir+'pnt.'+str(frequency))):
      target_list.append(sub_dir+'pnt.'+str(frequency))

if (len(target_list)):
    cmd='%s/uvcat vis=%s out=%s\n'%(env['MIRBIN'],','.join(target_list),sys.argv[-1])
else:
    cmd='echo not making '+sys.argv[-1]
print cmd
os.system(cmd)


#cmd='mv %s %s;\nmv %s %s\n'%(PhaseCal,sys.argv[-2],target_dir_name,sys.argv[-1])
#print cmd
#os.system(cmd)
os.system('rm -r %s %s'%(data_file,sub_dir))
