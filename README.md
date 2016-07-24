#UBUNTU 14.04 Server Edition Sıkılaştırma kılavuzu
===================================================
####*Bu sıkılaştırma klavuzunda Ubuntu 14.04 Server Edition'ı sıkılaştırmak için gerekli adımlar gösterilmektedir.*
___________________________________________________________________________________________________________________

###1. Kurulum sırasında yapılacak sıkılaştırmalar
   1.1. /tmp için ayrı bir partition oluşturma
   
      /tmp bütün kullanıcıların birlikte kullandığı ortak bir dizin olduğu için bu partition'ı ayrı tutmak
      yapılan saldırılarda diğer harddisk bölümlerine geçişi engellenmiş olur.
   1.2. /var için ayrı bir partition oluşturma
   
      /var dizini OS üzerinde çalışan servislerin çalıştığı ve dinamik data akışının gerçekleştiği dizindir.
      İçinde bulunduğu partition içerisinden müdahelede bulunulma riski bulunmaktadır. Ayrı bir partition 
      bu açıdan daha güvenlidir.

   1.3. /var/log için ayrı bir partition oluşturma
   
      /var/log dizini sistem servislerinin loglarının tutulduğu dizindir. Tutulan loglar çok hızlı şekilde
      büyümektedir. Kullanılan kaynağın buna göre ayarlanması için ayrılması büyük önem arz etmektedir.
      Servislerin bütün kayıtları loglara düşmektedir. Gerektiğinde kontrol edilebiliyor olması gerekmektedir.
