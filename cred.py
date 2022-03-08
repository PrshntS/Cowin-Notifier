file=open("C:\Cowin-Notifier\cred.txt",'r')
lines=file.readlines()
username=lines[0]
password=lines[1]
file.close()

print(username)
print(password)