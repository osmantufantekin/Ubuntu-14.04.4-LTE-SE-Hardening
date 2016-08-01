import os

score = 0
total = 48
test_number=1

test_result = open("test.txt", "w+")

shell= os.popen('grep "[[:space:]]/tmp[[:space:]]" /etc/fstab')
result = shell.read()
#/tmp kontrol
if (result !=''):
	test_result.write("1- /tmp'nin farkli partitionda olmasi	GECTI\n")
	score+=2
else:
	test_result.write("1- /tmp'nin farkli partitionda olmasi	GECMEDI\n")

shell = os.popen('grep "[[:space:]]/var[[:space:]]" /etc/fstab')
result = shell.read()
#/var kontrol
if (result !=''):
	test_result.write("2- /var'in farkli partitionda olmasi		GECTI\n")
	score+=2
else:
	test_result.write("2- /var'in farkli partitionda olmasi		GECMEDI\n")

#/home kontrol
shell = os.popen('grep "[[:space:]]/home[[:space:]]" /etc/fstab')
result = shell.read()
if (result !=''):
	test_result.write("3- /home'un farkli partitionda olmasi	GECTI\n")
	score+=2
else:
	test_result.write("3- /home'un farkli partitionda olmasi	GECMEDI\n")

#Otomatik mountingin kullanim disi olmasi
shell = os.popen('initctl show-config autofs')
result = shell.read()

if(result ==''):
	test_result.write('4- otomatik mounting kullanim disi	GECTI\n')
	score+=1
else:
	test_result.write('4- otomatik mounting kullanim disi	GECMEDI\n')

#bootloder user test
shell = os.popen('stat -c \"%u %g\" /boot/grub/grub.cfg | egrep \"^0 0\"')
result = shell.read()

if(result == ''):
	test_result.write('5- bootloader userlarin set edilmesi		GECTI\n')
	score+=1
else:
	test_result.write('5- bootloader userlarinin set edilmesi	GECMEDI\n')

#bootloader izin ayarlamalari
shell = os.popen('stat -L -c \"%a\" /boot/grub/grub.cfg | egrep \".00\"')
result = shell.read()

if(result == ''):
	test_result.write('6- bootloader izin ayarlamasi	GECTI\n')
	score+=2
else:
	test_result.write('6- bootloader izin ayarlamsi		GECMEDI\n')

#prelink test
shell = os.popen('dpkg -s prelink')
result = shell.read()
if ("not" in result or result == ''):
	test_result.write('7- prelink kullanim disi	GECTI\n')
	score+=1
else:
	test_result.write('7- prelink kullanim disi	GECMEDI\n')

#NIS test
shell = os.popen('dpkg -s nis')
result = shell.read()
if("not" in result or result == ''):
	test_result.write('8- nis kullanim disi		GECTI\n')
	score+=1
else:
	test_result.write('8- nis kullanim disi 	GECMEDI\n')

#rsh test
shell = os.popen('grep ^shell /etc/inetd.conf')
result = shell.read()

if(result == ''):
	test_result.write('9- rsh kullanim disi		GECTI\n')
	score+=1
else:
	test_result.write('9- rsh kullanim disi		GECMEDI\n')

#rshh client test
shell = os.popen('dpkg -s rsh-client')
result = shell.read()
if("not" in result or result ==''):
	test_result.write('10- rsh-client kullanim disi	 GECTI\n')
	score+=1
else:
	test_result.write('10- rsh-client kullanim disi	 GECMEDI\n')

#talk test
shell = os.popen('grep ^talk /etc/inetd.conf')
result = shell.read()
if(result ==''):
	test_result.write('10- talk kullanim disi	 GECTI\n')
	score+=1
else:
	test_result.write('10- talk kullanim disi	 GECMEDI\n')

#talk client test
shell = os.popen('dpkg -s talk')
result = shell.read()
if("not" in result or result==''):
	test_result.write('11- talk-client kullanim disi	GECTI\n')
	score+=1
else:
	test_result.write('11- talk-client kullanim disi	GECMEDI\n')

#telnet test
shell = os.popen('grep ^telnet /etc/inetd.conf')
result = shell.read()
if(result == ''):
	test_result.write('12- telnet kullanim disi	GECTI\n')
	score+=1
else:
	test_result.write('12- telnet kullanim disi	GECMEDI\n')

#tftp-server test
shell = os.popen('grep ^tftp /etc/inetd.conf')
result = shell.read()
if(result == ''):
	test_result.write('13- tftp kullanim disi	GECTI\n')
	score+=1
else:
	test_result.write('13- tftp kullanim disi	GECMEDI\n')

#chargen test
shell = os.popen('grep ^chargen /etc/inetd.conf')
result =shell.read()
if(result == ''):
	test_result.write('14- chargen kullanim disi 	GECTI\n')
	score+=2
else:
	test_result.write('14- chargen kullanim disi	GECMEDI\n')

#daytime test
shell = os.popen('grep ^daytime /etc/inetd.conf')
result = shell.read()
if(result ==''):
	test_result.write('15- daytime kullanimdisi	GECTI\n')
	score+=1
else:
	test_result.write('15- daytime kullanim disi	GECMEDI\n')

#echo test
shell = os.popen('grep ^echo /etc/inetd.conf')
result = shell.read()
if(result == ''):
	test_result.write('16- echo kullanim disi	GECTI\n')
	score+=1
else:
	test_result.write('16- echo kullanim disi 	GECMEDI\n')

#discard test
shell = os.popen('grep ^discard /etc/inetd.conf')
result = shell.read()
if(result ==''):
	test_result.write('17- discard kullanim disi 	GECTI\n')
	score+=1
else:
	test_result.write('17- discard kullanim disi 	GECMEDI\n')

#time test
shell = os.popen('grep ^time /etc/inetd.conf')
result = shell.read()
if(result ==''):
	test_result.write('18- time kullanim disi	GECTI\n')
	score+=1
else:
	test_result.write('18- time kullanim disi 	GECMEDI\n')

#rsyn test
shell = os.popen('grep ^RSYN ENABLE /etc/default/rsync')
result = shell.read()
if("false" in result):
	test_result.write('19- rsync kullanim disi 	GECTI\n')
	score+=1
else:
	test_result.write('19- rsync kullanim disi	GECMEDI\n')

#IP forwarding test
shell = os.popen('/sbin/sysctl net.ipv4.ip forward')
result = shell.read()
if("0" in result):
	test_result.write('20- IP forwarding devre disi		GECTI\n')
	score+=2
else:
	test_result.write('20- IP forwarding devre disi 	GECMEDI\n')

#supheli paket log test
shell = os.popen('/sbin/sysctl net.ipv4.conf.all.log martians')
result = shell.read()
if('1' in result):
	test_result.write('21- supheli paket log	GECTI\n')
	score+=2
else:
	test_result.write('21- supheli paket log	GECMEDI\n')

#broadcast ignore testi
shell = os.popen('/sbin/sysctl net.ipv4.icmp ignore broadcasts')
result = shell.read()
if('1' in result):
	test_result.write('22- broadcast ignore		GECTI\n')
	score+=1
else:
	test_result.write('22- broadcast ignore		GECMEDI\n')

#firewall aktif testi
shell =os.popen('ufw status')
result = shell.read()
if("active" in result):
	test_result.write('23- firewall aktif		GECTI\n')
	score+=3
else:
	test_result.write('23- firewall aktif		GECMEDI\n')

#audit test
shell = os.popen('dpkg -s auditd')
result = shell.read()
if("installed" in result):
	test_result.write('24- audit yuklu	GECTI\n')
	score+=2
else:
	test_result.write('24- audit yuklu 	GECEMEDI\n')

#audit butun loglar test
shell = os.popen('grep max_log_file_action /etc/audit/auditd.conf')
result = shell.read()
if("keep_logs" in result):
	test_result.write('25- butun loglarin tutulmasi 	GECTI\n')
	score+=2
else:
	test_result.write('25- butun loglarin tutulmasi		GECMEDI\n')

#audit immutable test
shell = os.popen('tail -n 1 /etc/audit/audit.rules')
result = shell.read()
if("-e 2" in result):
	test_result.write('26- audit immutable		GECTI\n')
	score+=2
else:
	test_result.write('26- audit immutable 		GECMEDI\n')

#cron aktif test
shell = os.popen('/sbin/initctl show-config cron')
result = shell.read()
if("start on runlevel[2345]" in result):
	test_result.write('27- cron aktif 	GECTI\n')
	score+=1
else:
	test_result.write('27- cron aktif	GECMEDI\n')

#PAM sifre tekrar testi(5 kez)
shell = os.popen('grep \"remember\" /etc/pam.d/common-password')
result =shell.read()
if("remember=5" in result):
	test_result.write('28- sifre tekrar testi	GECTI\n')
	score+=1
else:
	test_result.write('28- sifre tekrar testi	GECMEDI\n')

#ssh version 2 test
shell = os.popen('grep "^Protocol" /etc/ssh/sshd_config')
result =shell.read()
if("2" in result):
	test_result.write('29- ssh version 2	GECTI\n')
	score+=3
else:
	test_result.write('29- ssh version 2 	GECMEDI\n')

#ssh root login test
shell = os.popen('grep \"^PermitRootLogin\" /etc/ssh/sshd_config')
result = shell.read()
if("no" in result):
	test_result.write('30- ssh root login engellemesi	GECTI\n')
	score+=1
else:
	test_result.write('30- ssh root login engellemesi 	GECMEDI\n')

#parola yasam suresi testi(7 gun)
shell = os.popen('grep PASS MIN DAYS /etc/login.defs')
result = shell.read()
if("PASS_MIN_DAYS 7" in result):
	test_result.write('31- parola yasam suresi(7 gun)	GECTI\n')
	score+=1
else:
	test_result.write('31- parola yasam suresi(7 gun)	GECMEDI\n')

#/etc/passwd erisim testi
shell = os.popen('/bin/ls -l /etc/passwd')
result =shell.read()
if("-rw-r--r-- 1 root root" in result):
	test_result.write('32- /etc/passwd erisim	GECTI\n')
	score+=1
else:
	test_result.write('32- /etc/passwd erisim	GECMEDI\n')

#/etc/shadow erisim testi
shell = os.popen('/bin/ls -l /etc/shadow')
result =shell.read()
if("-rw--r----- 1 root shadow" in result):
	test_result.write('33- /etc/shadow erisim	GECTI\n\n\n')
	score+=1
else:
	test_result.write('33- /etc/shadow erisim	GECMEDI\n\n\n')

test_result.write(str(score))
test_result.write("/")
test_result.write(str(total))
test_result.close()

