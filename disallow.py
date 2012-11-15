#!/usr/bin/python

import time, subprocess, re, os, signal

def cleanlist(L):
	for n,l in reversed(list(enumerate(L))):
		if len(l)>0 and l[0]=='#': del L[n]
	if L[-1] == '': del L[-1]
	return L

myPID = os.getpid()
while True:
	with open('disallow_list') as fh:
		disallow_list = fh.read().split('\n')
	cleanlist(disallow_list)
	print 'disallowing:',disallow_list
	options = ['-s']
	if len(disallow_list) > 0:
		p = subprocess.Popen(['killall'] + options + disallow_list, stdout=subprocess.PIPE)
		(output,error) = p.communicate()
		output_lines = cleanlist(output.split('\n'))
		for line in output_lines:
			m = re.search(r'\d+$',line)
			if m: #print m.group()
				PID = int(m.group())
				if PID != myPID: # don't kill urself
					os.kill(PID, signal.SIGTERM)
	else:
		print 'Nothing to disallow.  Add program names to disallow_list, one line per program.'
	time.sleep(1)

