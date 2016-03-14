import os
os.chdir('./Databases/yalefaces')
directory = "Subject_"
for i in range(12,16):
	if not os.path.exists(directory+str(i)):
		os.makedirs(directory+str(i))