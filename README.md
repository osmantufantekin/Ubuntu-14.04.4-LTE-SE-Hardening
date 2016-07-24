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

   1.3. /var/log için ayrı bir partition oluşturma
   
      /var/log dizini sistem servislerinin loglarının tutulduğu dizindir. Tutulan loglar çok hızlı şekilde
      büyümektedir. Kullanılan kaynağın buna göre ayrılması büyük önem arz etmektedir. Servislerin bütün
      kayıtları loglara düşmektedir. Gerektiğinde kontrol edilebiliyor olması gerekmektedir.

   1.4 /home için ayrı bir partition oluşturma
   
      Yerel kullanıcılar için disk sağlama alanı sağlayan bu dizin OS'in servislerinden bağımsız tutulması
      gerekmektedir.
   
   1.5 Herkese açık dizinlerde Sticky Bit'in set edilmesi
   
      Kullanıcıların kendisine ait olmayan dizinler altındaki verilerin silinmesini ve isimlerinde değişiklik
      yapmasını engellenmesi gerekmektedir.
      
> \# df --local -P | awk {'if (NR!=1) print $6'} | xargs -I '{}' find '{}' -xdev -type d-perm -0002 2>/dev/null | xargs chmod a+t

   1.6 Otomatik Mountingin kullanım dışı bırakma
   
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
####4.1 Hazır gelen servislerin kapatılması
   >Servisler eğer OS üzerinde yapılan çalışmalar için önemli değilse kaldırılmalıdır. Bu kısımda dikkat
   >edilmesi gereken en önemli durum buna dikkat etmektir.

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

   4.1.6.
