#UBUNTU 14.04 Server Edition Sıkılaştırma kılavuzu
===================================================
####*Bu sıkılaştırma klavuzunda Ubuntu 14.04 Server Edition'ı sıkılaştırmak için gerekli adımlar gösterilmektedir.*
___________________________________________________________________________________________________________________

###1. Dosya Sistemi Sıkılaştırmaları
   1.1. /tmp için ayrı bir partition oluşturma
   
      /tmp bütün kullanıcıların birlikte kullandığı ortak bir dizin olduğu için bu partition'ı ayrı tutmak
      yapılan saldırılarda diğer harddisk bölümlerine geçişi engellenmiş olur.
   1.2. /var için ayrı bir partition oluşturma
   
      /var dizini OS üzerinde çalışan servislerin çalıştığı ve dinamik data akışının gerçekleştiği dizindir.
      İçinde bulunduğu partition içerisinden müdahelede bulunulma riski bulunmaktadır. Ayrı bir partition 
      bu açıdan daha güvenlidir.


   1.3 /home için ayrı bir partition oluşturma
   
      Yerel kullanıcılar için disk sağlama alanı sağlayan bu dizin OS'in servislerinden bağımsız tutulması
      gerekmektedir.
   
   1.4 Herkese açık dizinlerde Sticky Bit'in set edilmesi
   
      Kullanıcıların kendisine ait olmayan dizinler altındaki verilerin silinmesini ve isimlerinde değişiklik
      yapmasını engellenmesi gerekmektedir.
      
> \# df --local -P | awk {'if (NR!=1) print $6'} | xargs -I '{}' find '{}' -xdev -type d-perm -0002 2>/dev/null | xargs chmod a+t

   1.5 Otomatik Mountingin kullanım dışı bırakma
   
      USB, CD gibi otomatik mountlanan cihazların engellenmesi gerekmektedir.
      /etc/int/autofs.conf dosyası içinde ilk satır aşağıdaki gibi commentlenir.
   
> \# start on runlevel [2345]

###2. Boot Güvenlik Sıkılaştırmaları
   2.1 bootloader üzerinde User/Group'ların set edilmesi
   
      Root olmayan kullanıcıların dizinler üzerinde değişiklik yapmaması için gerekli sıkılaştırmadır.
      Aşağıdaki bash çalıştırılarak işlem gerçekleştirilir.

> \# chown root:root /boot/grub/grub.cfg
   
   2.2 bootloader configi üzerinde izinlerin ayarlanması
   
      Root parametrelerin değiştirilmesini ve görülmesini engelleme işlemidir. Root parametrelerinin
      okunması sistemdeki zayıflıkların görülmesine sebep olabilir. Aşağıdaki bash çalıştırılarak işlem
      gerçekleştirilir.

> \# chmod og-rwx /boot/grub/grub.cfg

   2.3 Boot Loader parolası ayarlanması
   
      Root parametrelerinin değiştirilmek istenilmesi durumunda paraloyla yetkisiz olan kullanıcıların
      engellenmesi gerekmektedir. Aşağıdaki bash çalıştırılarak gerçekleştirilir. 

>  \# grub-mkpasswd-pbkdf2   
>     Enter password: <password>   
>     Reenter password: <password>    
>     Your PBKDF2 is <encrypted-password>   

###3. Ek Process Sıkılaştırmaları

   3.1 Prelink'i devredışı bırakma
   
      Prelink daha hızlı başlangıçlar için binary'leri değiştirir. Binary'lere erişimin sağlanması engellenmesi
      gerekmektedir. Binary'leri normale döndürmek için aşağıdaki ilk bash çalıştırılır. Prelinki silmek için
      ikinci bash çalıştırılmalıdır.
   
> \# /usr/sbin/prelink -ua

> \# apt-get purge prelink

###4. İşletim Sistemi Servisleri Sıkılaştırmaları
   >Servisler eğer OS üzerinde yapılan çalışmalar için önemli değilse kaldırılmalıdır. Bu kısımda dikkat
   >edilmesi gereken en önemli durum buna dikkat etmektir.

####4.1 Hazır gelen servislerin kapatılması

   4.1.1 NIS'in devredışı bırakılması
   
      client-server içerikli bir servistir. Aşağıdaki bash kullanılarak kaldırılır.
> \# apt-get purge nis

   4.1.2. rsh server'ın devredışı bırakılması

      clear-text üzerinden haberleşen bir service'tir. /etc/inetd.conf içerisinde başında shell, login ve
      exec içeren satırlar comment yapılarak devredışı bırakılır.
   
>\#shell stream tcp nowait root /usr/sbin/tcpd /usr/sbin/in.rshd 
>\#login stream tcp nowait root /usr/sbin/tcpd /usr/sbin/in.rlogind 
>\#exec stream tcp nowait root /usr/sbin/tcpd /usr/sbin/in.rexecd

   4.1.3. rsh client'ın devredışı bırakılması

      rsh server'ın devredışı kalmasından sonra client da devredışı bırakılır. Aşağıdaki bash kullanılarak
      devredışı bırakılır.

> \# apt-get purge rsh-client rsh-reload-client

   4.1.4. Talk server'ın devredışı bırakılması
   
      Terminal üzerinden mesaj alınıp gönderilmesine yarayan servistir. /etc/inetd.conf içerisinde başında shell,
      login ve exec içeren satırlar comment yapılarak devredışı bırakılır.

> \# talk dgram udp wait nobody.tty /usr/sbin/in.talkd in.talkd 
> \# ntalk dgram udp wait nobody.tty /usr/sbin/in.ntalkd in.ntalkd

   4.1.5. Talk client'ın devredışı bırakılması

      talk server'ın devredışı kalmasından sonra client da devredışı bırakılır. Aşağıdaki bash kullanılarak
      devredışı bırakılır.

> \# apt-get purge talk

   4.1.5. Telnet server'ın devredışı bırakılması
   
      Telnet protokolü kullanılarak mesaj alıp vermeye yarayan servistir. /etc/inetd.conf
      telnet ile başlayan satır silinerek devredışı bırakılır.

> \# telnet stream tcp nowait telnetd /usr/sbin/tcpd /usr/sbin/in.telnetd

   4.1.5. tftp-server'ın devredışı bırakılması

      Dosya transfer protokolü olan tftp'nin devredışı bırakılması gerekmektedir. /etc/inet.conf içeresindeki
      tftp geçen bütün satırlar commentlenerek gerçekleştirilir.

> \# tftp stream tcp nowait root internal

#### 4.2 chargen'in devredışı bırakılması

      chargen, network debug ve test için kullanılan bir servistir. Bu servisin kapatılması uzaktan gelen
      saldırıları azaltır. /etc/inetd.conf içeresindeki chargen içeren satırlar commentlenerek devredışı 
      bırakılır.

> \# chargen stream tcp nowait root internal

#### 4.3 daytime'ın devredışı bırakılması

      Serverların tarih ve saat bilgilerini gönderen bir network servisidir. /etc/inetd.conf içerisindeki
      daytime içeren satırlar commentlenerek devredışı bırakılır.

>\# daytime stream tcp nowait root internal

#### 4.4 echo'nun devredışı bırakılması

      Debug ve test için kullanılan bir network servisidir. /etc/inetd.conf içerisindeki echo içeren
      satırlar commentlenerek devredışı bırakılır.
   
> \# echo stream tcp nowait root internal

#### 4.5 discard'ın devredışı bırakılması

      Aldığı bütün mesajları silen bir network servisidir. /etc/inetd.conf içerisindeki discard içeren
      bütün satırlan commentlenerek devredışı bırakılır.

> \# discard stream tcp nowait root internal

#### 4.6 time'ın devredışı bırakılması

      Serverların tarih ve saatini 32 bit integer şeklinde dönen bir network servisidir. /etc/inetd.conf
      içerisindeki time içeren satırlar commentlenerek devredışı bırakılır.

> \# time stream tcp nowait root internal

### 5. Özel amaçlı servislerin sıkılaştırılması
   >Servisler eğer OS üzerinde yapılan çalışmalar için önemli değilse kaldırılmalıdır. Bu kısımda dikkat
   >edilmesi gereken en önemli durum buna dikkat etmektir.
   
#### 5.1 FTP Serverın devredışı bırakılması

      File Transfer Protocol dosya transferinde kullanılan bir serverdır. /etc/init/vsfrpd.conf içerisindeki
      ilk satır commentlenerek devredışı bırakılır.

> \#start on runlevel [2345] or net-device-up IFACE!=lo

#### 5.2 HTTP Serverın devredışı bırakılması

      HTTP Web Server olarak kullanılan bir protokoldür. Atak genişliğini azaltmak için kapatılması gerekmektedir.
      /etc/rc*.d içerisindeki ilk satır commentlenerek devredışı bırakılır.

> \# rm /etc/rc*.d/S*apache2

#### 5.3 IMAP ve POP server'larının devredışı bırakılması

      IMAP ve POP Mail Serverlar olarak kullanılır. /etc/init/devecot.conf içeresindeki ilk satır commentlenerek
      devredışı bırakılır.

> \#start on runlevel [2345]

#### 5.4 rsync servisinin devredışı bırakılması

      Networkler ile sistem arasındaki dosyaların senkronize edilmesini sağlayan servistir. Clear-text bir protokol
      olduğu için tehlike arz etmektedir. /etc/default/rsync içerisindeki RSYNC_ENABLE satırını 'false' yaparak
      devredışı bırakılır.

> RSYNC_ENABLE=false

### 6. Network ve Firewall Ayarları

#### 6.1 IP Forwarding'i devredışı bırakma

      Server router olarak kullanılmıyorsa IP Forwarding'in devredışı bırakılması gerekmektedir. /etc/sysctl.conf
      içerisindeki net.ipb4.ip_forward parameter değerinin = olması gerekmektedir.

> net.ipv4.ip_forward=0

#### 6.2 Şüpheli gelen paketleri loglama

      Gelen paketlerde şüpheli olanların loglanmasını sağlamak gelen atakların takibini kolaylaştıracaktır.
      /etc/sysctl.conf içerisindeki net.ipv4.conf.all.log_martians ve net.ipv4.conf.default.log_martians değerleri
      1 yapılarak bu sağlanır.

> net.ipv4.conf.all.log_martians=1
> net.ipv4.conf.default.log_martians=1

#### 6.3 Broadcast isteklerinin ignore edilmesi

      ICMP broadcast mesajlarıyla yapılabilecek bir saldırıyı engellemek için ignore edilmesi gerekmektedir.
      /etc/sysctl.conf içerisindeki net.ipv4.icmp_echo_ignore_broadcasts değeri 1 yapılarak ignore edilir.

> net.ipv4.icmp_echo_ignore_broadcasts=1

#### 6.4 TCP SYN Cookies'in etkinleştirilmesi

      DOS saldırılarında kullanılan SYN Flood tekniği için kullanılması gereken bir sıkılaştırmadır.
      DOS saldırsı altında da gerekli yerlere mesajların gönderilmesi için TCP SYN Cookies'in etkinleştirilmesi
      gerekmektedir. /etc/sysctl.conf içerisinde net.ipv4.tcp_syncookies parametresi 1 yapılmalıdır.

>net.ipv4.tcp_syncookies=1

#### 6.5 Yaygın olamyan Network Protokollerinin devredışı bırakılması

      DCCP, SCTP, RDS, TIPC gibi protokollerin devredışı bırakılması bunlardan kaynaklanacak açıkların
      kullanılmasını engellemektedir.
   
#### 6.6 Firewall'un aktif olduğundan emin olunması

      Firewallar her yerde olduğu gibi Ubuntu üzerinde de gelen bağlantıların limitlenerek savunma sistemini
      güçlendirmeyi sağlamaktadır ve her sistemde olduğu gibi burda da Firewall'un açık olması en büyük
      sıkılaştırmaların başında gelmektedir. Aşağıdaki bash kullanılarak aktif değilse aktif hale getirilir.

> \# ufw enable

### 7. Logging ve Auditing

      log ve audit sistem üzerinde gerçekleştirilen değişiklikler, kullanıcılar ile ilgili bilgiler ve hareketleri
      tutan bir yapıdır. Saldırı tespitinde kullanılan en önemli unsurlardan biridir.

#### 7.1 Bütün Auditing bilgilerinin tutulması

      auditd default olarak maksimum 4 tane log tutmaktadır ve bunun genişletilmesi gerekmektedir.
      /etc/audit/auditd.conf içerisine aşağıdaki satır eklenerek gerçekleştirilir.

>  max_log_file_action = keep_logs

#### 7.2 auditd servisinin yüklenmesi ve kullanılabilir hale getirilmesi

      Sistem olaylarını kaydının tutulması için gerekli sıkılaştırmadır. Aşağıdaki bash ile gerçekleştirilir.

> \# apt-get install auditd

#### 7.3 Tarih ve Saati değişikliği yapan olayların kaydedilmesi

      Sistemde yapılan tarih ve saat değişiklikleri yapılan bir saldırının tespitini zorlaştırmak için kullanılan
      bir metotdur. Bunların kaydedilmesi kayıtları daha verimli kullanılmasını sağlamaktadır. 64 bit için aşağıdaki
      satırlar /etc/audit/audit.rules 'a eklenir.

> -a always,exit -F arch=b64 -S adjtimex -S settimeofday -k time-change   
> -a always,exit -F arch=b32 -S adjtimex -S settimeofday -S stime -k time-change   
> -a always,exit -F arch=b64 -S clock_settime -k time-change   
> -a always,exit -F arch=b32 -S clock_settime -k time-change   
> -w /etc/localtime -p wa -k time-change   
> \# Execute the following command to restart auditd   
> \# pkill -P 1-HUP auditd   

      32 bit için /etc/audit/audit.rules 'a aşağıdaki satırlar eklenir.

> -a always,exit -F arch=b32 -S adjtimex -S settimeofday -S stime -k time-change   
> -a always,exit -F arch=b32 -S clock_settime -k time-change   
> -w /etc/localtime -p wa -k time-change   
> \# Execute the following command to restart auditd   
> \# pkill -P 1-HUP auditd   

#### 7.4 Oturum açma ve kapatma olaylarının kaydedilmesi

      Özellikle Brute Force saldırılarının tespit edilmesi için uygulanması gereken sıkılaştırmadır. 
      /etc/audit/audit.rules dosyasına aşağıdaki satırlar eklenerek uygulanır.

> -w /var/log/faillog -p wa -k logins   
> -w /var/log/lastlog -p wa -k logins   
> -w /var/log/tallylog -p wa -k logins   
> \# Execute the following command to restart auditd   
> \# pkill -HUP -P 1 auditd   

#### 7.5 Dosyalara olan başarısız ve yetkisiz açma girişimlerinin kaydının tutulması

      İzinsiz olunan dosyaları açmaya çalışan kullanılar ya da dışarıdan yapılan saldırıların tespiti
      için bu kayıtların da tutulması tespit için kolaylık sağlamaktadır.
      64 bit için /etc/audit/audit.rules dosyasına aaşağıdaki satırlar eklenir.

> -a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate \   
> -F exit=-EACCES -F auid>=500 -F auid!=4294967295 -k access   
> -a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate \   
> -F exit=-EACCES -F auid>=500 -F auid!=4294967295 -k access   
> -a always,exit -F arch=b64 -S creat -S open -S openat -S truncate -S ftruncate \   
> -F exit=-EPERM -F auid>=500 -F auid!=4294967295 -k access   
> -a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate \   
> -F exit=-EPERM -F auid>=500 -F auid!=4294967295 -k access   
> \# Execute the following command to restart auditd   
> \# pkill -HUP -P 1 auditd

      32 bit için /etc/audit/audit.rules dosyasına aşağıdaki satırlar eklenir.

> -a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate \   
> -F exit=-EACCES -F auid>=500 -F auid!=4294967295 -k access   
> -a always,exit -F arch=b32 -S creat -S open -S openat -S truncate -S ftruncate \   
> -F exit=-EPERM -F auid>=500 -F auid!=4294967295 -k access   
> \# Execute the following command to restart auditd   
> \# pkill -HUP -P 1 auditd   

#### 7.6 Sistem Adminliği değişikliklerinin kaydedilmesi(sudolog)

      Sistem admini tarafından yapılan değişikliklerin kaydedilmesine olanak tanır. 
      /etc/audit/audit.rules dosyasına aşağıdaki satırlar eklenerek gerçekleştirilir.

> -w /var/log/sudo.log -p wa -k actions   
> \# Execute the following command to restart auditd   
> \# pkill -HUP -P 1 auditd   

#### 7.7 Audit Konfigürasyonlarının immutable yapılması

      Audit sisteminin immutable yapılması yetkili olmayan kullanıcılar değişiklik yapamaması
      için önemli bir sıkılaştırmadır. /etc/audit/audit.rules dosyasına aşağıdaki satır eklenerek
      uygulanır.

> -e 2

#### 7.8 AIDE kurulumu

      Kritik dosyalardaki değişiklikleri görülmesini sağlayan bir araçtır. Aşağıdaki bash ile etkinleştirilir.

> \# apt-get install aide   
> \# aideinit   
> \# cp /var/lib/aide/aide.db.new /var/lib/aide/aide.db   

### 8. System Access, Authentication and Authorization

#### 8.1 cron'un aktifleştirilmesi

      batch işlemlerini uygulayan araçtır. /etc/init/cron.conf dosyasındaki ilk satır aşağıdaki gibi yapılmalıdır.

> start on runlevel [2345]

#### 8.2 PAM'ın aktifleştirilmesi

      PAM (Pluggable Authentication Modules) Unix sistemlerinde authentication modüllerinin yazıldığı araçtır.

##### 8.2.1 Şifrelemenin nasıl yapılacağına karar verilmesi

      PAM ile şifrelemenin kısıtları ve kaç denemeye kadar müsade edileceğinin yapılması gerekmektedir.
      /etc/pam.d/common-password içerisindeki pam_cracklib.so parametresi aşağıdaki gibi ayarlanmalıdır.

> password required pam_cracklib.so retry=3 minlen=14 dcredit=-1 ucredit=-1 ocredit=-1 lcredit=-1

##### 8.2.2 Şifrenin tekrar kullanımının kısıtlanması

      Aynı şifrenin tekrar kullanılmasını engellemek önemli sıkılaştırmalardan bir tanesidir.
      /etc/pam.d/common-password içeresindeki pam_unix.so remember parametresi aşağıdaki gibi set edilir.

> password sufficient pam_unix.so remember=5

#### 8.3 SSH Ayarlamaları

      SSH paketlerin şifrelenerek gönderilmesini sağlayan bir protokoldür.

##### 8.3.1 SSH versiyonunun 2 yapılması

      /etc/ssh/sshd_config içerisindeki Protocol parametresi aşağaıdaki gibi set edilir.

> Protocol 2

##### 8.3.2 SSH'a root olarak erişimin kapatılması

      Root olarak erişimin engellenmesi sudo ve su ile yapılabilecek değişiklikleri kısıtlar ve audit
      için daha düzgün bir loglamaya olanak sağlar. /etc/ssh/sshd_config içerisinde aşağıdaki değişilik
      yapılarak uygulanır.

> PermitRootLogin no

### 9. Kullanıcı hesapları sıkılaştırmaları

####9.1 Parola sıkılaştırmaları

##### 9.1.1 Parolanın yaşam süresinin ayarlanması

      /etc/login.defs içeresindeki PASS_MAX_DAYS parametresi aşağıdaki gibi değiştirilerek uygulanır.

> PASS_MAX_DAYS 90

### 10. Sistem Dosyalarına erişim sıkılaştırmaları

#### 10.1 /etc/passwd'a erişimin ayarlanması

      Parolaların erişimin engellenmesi dışarıdan gelebilecek tehditleri azaltmaktadır. Aşağıdaki bash
      uygulanarak erişim izni ayarlanır.

> /bin/chmod 644 /etc/passwd

#### 10.2 /etc/shado'a erişimin ayarlanması

      Kullanıcılarla ilgili verilerin tutulduğu dosyaya erişimin engellenmesi öenmli bir sıkılaştırmadır.
      Aşağıdaki bash çalıştırılarak erişim izni ayarlanır.

> /bin/chmod o-rwx,g-rw /etc/shadow

