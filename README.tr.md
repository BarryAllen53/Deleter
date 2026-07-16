Exit code: 0
Wall time: 0.3 seconds
Output:
# Deleter

[English documentation](README.md) · [Deutsche Dokumentation](README.de.md)

Deleter, erişilebilir depolama analizi ve güvenli temizlik incelemesi için geliştirilmiş bir Windows masaüstü uygulamasıdır. Büyük dosyaları ve yüklü programları gösterirken Windows için kritik yolları teknik olarak korur.

## Durum

0.2.0 sürümü ilk işlevsel genel sürümdür. Korumalı sistem taraması, doğrulanmış Geri Dönüşüm Kutusu temizliği, desteklenen kaldırma işlemleri, dışa aktarma, erişilebilirlik ve simülasyon modu içerir.

## Özellikler

- Arka planda artımlı tarama yapan Programlar ve Dosyalar sekmeleri.
- Kilitli ve erişilemeyen öğelerle çoklu seçim.
- 500 MB'den başlayan boyut filtresi.
- Duraklatma, devam ettirme ve iptal.
- İngilizce, Almanca ve Türkçe arayüz.
- Yerel Qt klavye erişilebilirliği ve Accessible Output 2 duyuruları.
- ACL farkındalıklı Windows hata yönetimi ve UAC desteği.
- Doğrulanmış temizlik, onaydan sonra uygun dosyaları Windows Geri Dönüşüm Kutusu'na taşır; simülasyon modu inceleme için kullanılabilir.
- Doğrulanmış komut planlama ve yalıtılmış çalıştırma ile Kayıt Defteri ve Microsoft Store/AppX kaldırma sağlayıcıları.
- Tarama sonuçları için JSON ve CSV dışa aktarma.

## Güvenlik

Büyük dosyalar otomatik olarak gereksiz kabul edilmez. Windows, önyükleme, sürücü, kurtarma, güvenlik, paket, program, reparse point ve belirsiz ACL alanları kilitli veya erişilemez kalır. Uygulama sahiplik devralmaz ve ACL değiştirmez.

## Erişilebilirlik, diller ve gereksinimler

Qt'nin yerel rollerini, adlarını, odak sırasını ve onay kutusu durumlarını kullanır. Önemli tarama ve uyarı olayları, mevcutsa Accessible Output 2 ile duyurulur. İngilizce, Deutsch ve Türkçe desteklenir. Kaynak çalıştırma için Windows 10 veya 11 ve Python 3.14.5 gerekir.

## Kurulum ve kullanım

Normal kullanıcılar Releases sayfasındaki taşınabilir ZIP'i indirebilir. Kaynaktan başlatmak için `run.bat` dosyasını çalıştırın; sanal ortamı oluşturur, bağımlılıkları kurar ve `python -m app` komutunu çalıştırır. Uygulama açılır açılmaz sistem taraması başlar. Dosyalar boyut filtresine göre kademeli gösterilir; programlar desteklenen Windows kaynaklarından okunur. Kilitli öğelerin onay kutuları etkinleştirilemez.

## Gizlilik, sınırlamalar ve katkı

Dosya listeleri, yollar, program bilgileri ve kullanım verileri cihazdan dışarı gönderilmez. Kalıcı silme bilerek sunulmaz; temizlik doğrulanmış ve onaylanmış Geri Dönüşüm Kutusu taşımasıyla sınırlıdır. Sertifika Secret'ları ayarlandığında imza release iş akışı tarafından etkinleştirilir. Ayrıntılar [ROADMAP.md](ROADMAP.md) içindedir. Katkılar [CONTRIBUTING.md](CONTRIBUTING.md) ile, güvenlik sorunları ise [SECURITY.md](SECURITY.md) içindeki GitHub Security Advisories yöntemiyle bildirilmelidir.

## Lisans

Deleter [MIT Lisansı](LICENSE) ile yayımlanır.

