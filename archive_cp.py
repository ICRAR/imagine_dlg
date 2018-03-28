import os,sys
work_dir=sys.argv[0].find('/')
if (work_dir>-1):
  work_dir=sys.argv[0].rindex('/')
  work_dir=sys.argv[0][0:work_dir]
else:
  work_dir='.'
os.chdir(work_dir)
execfile('init.py')

#os.system('rm -r '+sys.argv[-1][0:len(sys.argv[-1])-15)+'*')
#os.system('rm -r /tmp/daliuge_tfiles/2018-03-1*')

if (len(files)!=len(sys.argv[2:len(sys.argv)])):
    cmd='Mis-match between scatter %d and inputs %d\n'%(len(sys.argv[2:-1]),len(files))
    print(cmd)
#
for i in range(len(files)):
    files[i]=par['data_dir']+'/'+files[i]+'.'+par['project']
    if (i<len(sys.argv)-2):
        #os.system('rm -r '+sys.argv[i+2])
        #os.mkdir(sys.argv[i+2])
        #cmd='cp  -v %s %s/%s\n'%(files[i],sys.argv[i+2],sys.argv[i+2])
        cmd='rsync -v %s %s\n'%(files[i],sys.argv[i+2])
        print(cmd)
        os.system(cmd)

#cmd='uvcat vis=%s out=%s\n'%(','.join(files),sys.argv[2])
#cmd='uvcat vis=%s out=%s\n'%(','.join(files),sys.argv[2])
#print cmd


