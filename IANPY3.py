#! /usr/bin/python
import subprocess
import os
import time
import numpy as np
from multiprocessing import Pool

cmd = raw_input('Please enter the FreeSurfer commands you\'d like to run \n (options: recon1, pial, recon23, reconcp, lgi, gcut) : ')
proc = raw_input('Please enter the number of parallel processes you\'d like to run: ')

# Parallel computation:
def makelist():
	a = subprocess.getstatusoutput('echo $SUBJECTS_DIR')[1]
	b = os.listdir(a)
	b.sort()
	return a,b


global counter
counter = 0
def cb(r):
	global counter
	print(counter, r)
	counter +=1

if cmd == 'recon1':
	def IAN(M):
		os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
		os.system('recon-all -s ' + M + ' -autorecon1')
		os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Completed-AR1')
elif cmd == 'gcut':
	def IAN(M):
		os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
		os.system('recon-all -skullstrip -clean-bm -gcut -subjid ' + M)
		os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../AR1-Complete')
elif cmd == 'qdec':
	def IAN(M):
		os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
		os.system('recon-all -s ' + M + ' -qcache')
		os.system('recon-all -s ' + M + ' -qcache -measure pial_lgi' )
		os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Completed-QDEC')
elif cmd == 'pial':
	def IAN(M):
		os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
		os.system('recon-all -s ' + M + ' -autorecon-pial')
		os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Completed-23')
elif cmd == 'lgionly':
	def IAN(M):
		os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
		os.system('recon-all -s ' + M + ' -localGI')
		os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Completed-HSF')
elif cmd == 'reconall':
	def IAN(M):
		os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
		os.system('recon-all -s ' + M + ' -all')
		os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Completed')
elif cmd == 'recon23':
	def IAN(M):
		os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
		os.system('recon-all -s ' + M + ' -autorecon2 -autorecon3')
		os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Completed-23')
elif cmd == 'reconcp':
	def IAN(M):
		os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
		os.system('recon-all -s ' + M + ' -autorecon2-cp' + ' ' + '-autorecon3' )
		os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Completed-23')
elif cmd == 'lgi':
	def IAN(M):
		os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
		os.system('recon-all -s ' + M + ' -localGI')
		#os.system('recon-all -s ' + M + ' -hippo-subfields')
		os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Completed-HSF')
elif cmd == 'First':
	def IAN(M):
		if M[-10:] == '_t1.nii.gz':
			os.system('mkdir ' + M[:6])
			os.system('mv ' + M + ' ' + M[:6])
			os.system('run_first_all ' + '-i ' + a + '/'+ M[:6] +'/'+ M + ' ' + ' -o ' + a + '/' + M[:6] +  '/' + M  + ' -s L_Amyg,L_Hipp,R_Amyg,R_Hipp')
			#os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Images')
elif cmd == 'hsf':
        def IAN(M):
                os.system('rm ' + a + '/' + M + '/scripts/IsRunning.lh+rh')
                os.system('recon-all -s ' + M + ' -hippo-subfields')
                os.system('mv ' + a + '/' + M + ' ' + a + '/' + '../Completed-HSF')
	
def Proc(proc,IAN,a,b):
	po = Pool(processes=int(proc))
	for i in b:
		try:
			po.apply_async(IAN,(i,),callback=cb)
		except(Exception,e):
			continue
	po.close()
	po.join()
#	print counter

a,b = makelist()
while len(b) != 0:
	Proc(proc,IAN,a,b)
	a,b = makelist()
