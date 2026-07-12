"""
PARS Takımı — Kategori bazlı mail şablonları
Kaynak listedeki 23 kategori tam olarak eşleştirildi.
Maddi: 1,5,6,7,8,9,10,11
Malzeme/Parça + Maddi: 2,3,4,12-23 (teknokentler dahil)
"""
# LOGO_B64 artık kullanılmıyor — Drive linki kullanılıyor

# Kategori → (tip, kısa_ad) eşlemesi
# tip: "maddi" | "malzeme" | "her_ikisi"
KATEGORI_MAP = {
    "savunma sanayii":          ("her_ikisi", "savunma"),
    "ağır sanayi":              ("her_ikisi", "savunma"),
    "endüstriyel otomasyon":    ("malzeme",   "otomasyon"),
    "motor ve sürücü":          ("malzeme",   "otomasyon"),
    "yapay zeka":               ("malzeme",   "yazilim"),
    "yazılım":                  ("malzeme",   "yazilim"),
    "simülasyon":               ("malzeme",   "yazilim"),
    "imalat":                   ("malzeme",   "imalat"),
    "talaşlı":                  ("malzeme",   "imalat"),
    "3d baskı":                 ("malzeme",   "imalat"),
    "kitap":                    ("maddi",     "yayin"),
    "yayın":                    ("maddi",     "yayin"),
    "yiyecek":                  ("maddi",     "gida"),
    "gıda":                     ("maddi",     "gida"),
    "restoran":                 ("maddi",     "gida"),
    "kafe":                     ("maddi",     "gida"),
    "otel":                     ("maddi",     "otel"),
    "ilaç":                     ("maddi",     "ilac"),
    "farma":                    ("maddi",     "ilac"),
    "giyim":                    ("maddi",     "giyim"),
    "tekstil":                  ("maddi",     "giyim"),
    "elektronik":               ("her_ikisi", "elektronik"),
    "akıllı cihaz":             ("her_ikisi", "elektronik"),
    "otomotiv":                 ("her_ikisi", "otomotiv"),
    "teknokent":                ("malzeme",   "teknokent"),
    "cyberpark":                ("malzeme",   "teknokent"),
    "bilişim vadisi":           ("malzeme",   "teknokent"),
    "teknopark":                ("malzeme",   "teknokent"),
    "atap":                     ("malzeme",   "teknokent"),
    "ulutek":                   ("malzeme",   "teknokent"),
    "muhammed hoca":            ("her_ikisi", "savunma"),
}

def _kategori_belirle(sektor: str):
    """Sektör metninden kategori tipini ve şablon adını döndürür."""
    s = sektor.lower()
    for anahtar, (tip, sablon) in KATEGORI_MAP.items():
        if anahtar in s:
            return tip, sablon
    return "maddi", "genel"

def get_template(kategori, sirket, yetkili, ozel_not, gonderen_ad, takim_mail):
    tip, sablon = _kategori_belirle(kategori)
    fn = SABLONLAR.get(sablon, _genel)
    return fn(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip)

def _html(konu, govde_icerik, gonderen_ad, takim_mail, yetkili, sirket=""):
    konu = f"[{gonderen_ad.split()[0].upper()}] {konu}"
    selamlama = f"Sayın {sirket} Yetkilileri,"
    html = f"""<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#222;line-height:1.7;max-width:620px">
<p>{selamlama}</p>
{govde_icerik}
<p>Saygılarımla,</p>
<table cellpadding="0" cellspacing="0" style="margin-top:16px;border-top:2px solid #1F3864;padding-top:12px">
  <tr>
    <td style="padding-right:14px;vertical-align:middle">
      <img src="https://drive.google.com/uc?export=view&id=11wKCezNGTzghlakfTrAtQPRoH68M1GVl" width="64" height="64" alt="PARS IKA" style="border-radius:50%;border:2px solid #1F3864"/>
    </td>
    <td style="vertical-align:middle;font-size:13px;color:#222;line-height:1.6">
      <strong style="font-size:14px;color:#1F3864">{gonderen_ad}</strong><br>
      <span style="color:#555">TOBB ETÜ PARS Takımı — TEKNOFEST 2026 İKA</span><br>
      <a href="mailto:{takim_mail}" style="color:#2E75B6;text-decoration:none">{takim_mail}</a>
    </td>
  </tr>
</table>
</body></html>"""
    return konu, html

def _destek_cumlesi(tip):
    return "maddi sponsorluk"

def _savunma(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın savunma sanayiindeki öncü konumunu ve yerli teknolojiye katkısını yakından takip ediyoruz."
    destek = _destek_cumlesi(tip)
    icerik = f"""<p>{giris}</p>
<p>Bizler, TOBB ETÜ bünyesinde TEKNOFEST 2026 <strong>İnsansız Kara Aracı (İKA)</strong> yarışmasına katılan <strong>PARS Takımıyız</strong>. Otonom kara aracımız, Kritik Tasarım Raporu'nu <strong>88,75 puan</strong> ile tamamlayarak TEKNOFEST maddi desteği kazandı; şu an üretim ve entegrasyon aşamasındayız.</p>
<p>Savunma teknolojileri alanında {sirket} gibi köklü bir kurumun yanımızda olması, projemizin hem teknik olgunluğuna hem de kurumsal görünürlüğüne doğrudan katkı sağlayacaktır. <strong>{destek.capitalize()}</strong> kapsamında iş birliği değerlendirmenizi rica ederiz. Karşılığında araç üzeri logo, sosyal medya iş birlikleri ve etkinlik görünürlüğü sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 İKA Sponsorluk Teklifi", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _otomasyon(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın endüstriyel otomasyon ve sürücü sistemleri alanındaki teknik birikimini projemizle buluşturmak istiyoruz."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışmasında otonom bir kara aracı geliştiriyoruz. KTR aşamasını <strong>88,75 puan</strong> ile geçerek üretim hakkı kazandık. Aracımızın tahrik sistemi, motor sürücüleri ve enerji yönetimi bileşenleri kritik öneme sahip.</p>
<p>{sirket}'ın ürün ve sistemleri, aracımızın hareket ve kontrol altyapısına doğrudan entegre edilebilecek niteliktedir. <strong>Maddi sponsorluk</strong> kapsamında iş birliği yapmaktan büyük memnuniyet duyarız. Karşılığında araç üzeri logo ve sosyal medya görünürlüğü sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 İKA | Teknik Bileşen Sponsorluğu", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _yazilim(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın yapay zeka ve yazılım alanındaki yetkinliklerini projemizin otonom karar sistemiyle buluşturmak istiyoruz."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışmasında yapay zeka destekli otonom bir kara aracı geliştiriyoruz. KTR'yi <strong>88,75 puan</strong> ile tamamladık; navigasyon, görüntü işleme ve karar alma katmanlarımız aktif geliştirme sürecinde.</p>
<p>{sirket}'ın yazılım altyapısı, simülasyon araçları veya AI çözümleri projemizin teknik kabiliyetini doğrudan güçlendirebilir. <strong>Maddi sponsorluk</strong> kapsamında iş birliği değerlendirmelerinizi bekliyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 İKA | Yazılım & AI Sponsorluğu", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _imalat(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın imalat ve üretim teknolojileri alanındaki yetkinliği, aracımızın fiziksel üretiminde kritik bir ortak olabileceğinizi gösteriyor."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışması kapsamında otonom kara aracımızın şasi imalatı ve mekanik entegrasyon aşamasındayız. KTR'yi <strong>88,75 puan</strong> ile geçtik.</p>
<p>Talaşlı imalat, 3D baskı veya CNC işleme hizmetleri; aracımızın fiziksel üretiminde doğrudan kullanılacaktır. <strong>Maddi sponsorluk, imalat hizmeti veya malzeme desteği</strong> karşılığında araç üzeri logo, sosyal medya görünürlüğü ve etkinlik katılımı sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 İKA | İmalat & Üretim Sponsorluğu", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _yayin(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın bilim ve teknoloji yayınlarına verdiği değeri biliyor; bu misyonla örtüşen projemiz için destek talep ediyoruz."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İnsansız Kara Aracı yarışmasına katılan 13 kişilik genç mühendis ekibiyiz. KTR'yi <strong>88,75 puan</strong> ile tamamlayarak üretim aşamasına geçtik.</p>
<p>Teknik kaynak ve mühendislik kitapları ekibimizin hem yarışma sürecine hem de mesleki gelişimine katkı sağlayacaktır. <strong>Maddi sponsorluk</strong> karşılığında sosyal medya görünürlüğü, logo yerleşimi ve etkinlik iş birlikleri sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 | Sponsorluk Teklifi", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _gida(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın Türkiye'nin önde gelen markalarından biri olarak genç projelere verdiği değeri biliyor ve bu süreçte yanımızda görmek istiyoruz."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışmasına katılan 13 kişilik bir mühendislik ekibiyiz. KTR aşamasını <strong>88,75 puan</strong> ile başarıyla tamamladık.</p>
<p>Yarışma sürecinde ekibimizin sahada ve atölyede geçirdiği yoğun çalışma dönemlerinde <strong>maddi sponsorluk</strong>; hem motivasyonumuzu hem de markanızın genç nesildeki görünürlüğünü artıracaktır. Sosyal medya paylaşımları, etkinlik görünürlüğü ve araç üzeri marka yerleşimi sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 | Sponsorluk Teklifi", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _otel(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın Türkiye'nin köklü turizm markalarından biri olarak genç mühendislere destek potansiyelini değerlendirmek istiyoruz."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışmasına katılan 13 kişilik ekibimiz, yarışma finali için konaklama ihtiyacı duymaktadır. KTR'yi <strong>88,75 puan</strong> ile tamamladık.</p>
<p><strong>Maddi sponsorluk</strong> karşılığında; sosyal medya görünürlüğü, araç üzeri ve etkinlik alanı logo yerleşimi ile TEKNOFEST platformunda marka bilinirliği sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 | Sponsorluk Teklifi", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _ilac(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın AR-GE ve inovasyon kültürünün genç mühendislik projelerine de yansımasını umut ediyoruz."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışmasına katılan 13 kişilik bir ekibiz. KTR'yi <strong>88,75 puan</strong> ile tamamladık.</p>
<p>AR-GE odaklı kurumsal kültürünüzle örtüşen projemize <strong>maddi destek</strong>; ekibimizin yarışma sürecini başarıyla tamamlamasına doğrudan katkı sağlayacaktır. Karşılığında marka görünürlüğü, sosyal medya iş birlikleri ve etkinlik katılımı sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 | Sponsorluk Teklifi", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _giyim(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın güçlü marka kimliğini TEKNOFEST platformunda genç mühendislerle buluşturmak istiyoruz."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışmasına katılan 13 kişilik ekibimiz, yarışma boyunca binlerce izleyici ve medya önünde yer almaktadır. KTR'yi <strong>88,75 puan</strong> ile tamamladık.</p>
<p><strong>Maddi sponsorluk</strong>; {sirket} markasını Türkiye'nin en büyük teknoloji platformunda genç nesille buluşturacaktır. Araç üzeri logo, sosyal medya görünürlüğü ve etkinlik iş birlikleri sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 | Sponsorluk Teklifi", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _elektronik(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın akıllı cihaz ve teknoloji alanındaki vizyonunu, otonom sistemler geliştiren ekibimizle buluşturmak istiyoruz."
    destek = _destek_cumlesi(tip)
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışmasında yapay zeka destekli otonom bir kara aracı geliştiriyoruz. KTR'yi <strong>88,75 puan</strong> ile tamamladık.</p>
<p>Aracımızın bilgisayar, sensör ve gömülü sistem ihtiyaçları kapsamında <strong>{destek}</strong> değerlendirmenizi bekliyoruz. {sirket}'ın ürünlerinin sahada çalışır hâlde sergilenmesi, marka için güçlü bir tanıtım fırsatı sunacaktır.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 İKA | Teknoloji Sponsorluğu", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _otomotiv(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın otonom araç ve mobilite teknolojilerine verdiği stratejik önemi biliyor; bu vizyonla örtüşen projemiz için destek talep ediyoruz."
    destek = _destek_cumlesi(tip)
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışmasında otonom sürüş algoritmaları ve araç kontrolü üzerine çalışıyoruz. KTR'yi <strong>88,75 puan</strong> ile tamamladık.</p>
<p>Otomotiv mühendisliği ve otonom sistemler alanındaki örtüşme; {sirket} ile doğal bir iş birliği zemini oluşturuyor. <strong>{destek.capitalize()}</strong> kapsamında değerlendirmenizi bekliyoruz. Araç üzeri logo, sosyal medya ve etkinlik görünürlüğü sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 İKA | Otomotiv Sponsorluğu", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _teknokent(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip):
    giris = f"{sirket}'ın teknoloji ekosistemindeki konumunu ve inovasyon odaklı yaklaşımını yakından takip ediyoruz."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İKA yarışmasında yapay zeka ve otonom sistemler üzerine çalışan 13 kişilik bir mühendislik ekibiyiz. KTR'yi <strong>88,75 puan</strong> ile tamamlayarak üretim aşamasına geçtik.</p>
<p>{sirket}'ın yazılım, donanım veya sistem entegrasyon yetkinlikleri; projemizin teknik gelişimine doğrudan katkı sağlayabilir. <strong>Maddi sponsorluk</strong> kapsamında iş birliği yapmaktan memnuniyet duyarız. Karşılığında araç üzeri logo, sosyal medya görünürlüğü ve etkinlik katılımı sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 İKA | Teknoloji Sponsorluğu", icerik, gonderen_ad, takim_mail, yetkili, sirket)

def _genel(sirket, yetkili, ozel_not, gonderen_ad, takim_mail, tip="maddi"):
    giris = f"{sirket}'ın sektördeki güçlü konumunu ve vizyonunu biliyor; bu süreçte yanımızda görmek istiyoruz."
    icerik = f"""<p>{giris}</p>
<p>TOBB ETÜ <strong>PARS Takımı</strong> olarak TEKNOFEST 2026 İnsansız Kara Aracı yarışmasına katılıyoruz. Kritik Tasarım Raporumuzu <strong>88,75 puan</strong> ile tamamlayarak TEKNOFEST desteği aldık ve üretim aşamasındayız.</p>
<p>{sirket} gibi köklü bir kurumun desteğiyle projemizi çok daha ileriye taşıyabileceğimize inanıyoruz. <strong>Maddi sponsorluk</strong> karşılığında araç üzeri logo, sosyal medya iş birlikleri ve etkinlik görünürlüğü sunuyoruz.</p>
<p>Ekte sunduğumuz <strong>Sponsorluk Dosyamızı</strong> incelemeniz, talebimizi ilgili birimlerinize ulaştırmanız ve projemizle ilgili olası bir iş birliğinin değerlendirilmesi hususunda destekleriniz bizi çok mutlu edecektir.</p>
<p style="font-size:13px;color:#555">📎 Teknik detaylar için Kritik Tasarım Raporumuza (KTR) buradan ulaşabilirsiniz: <a href="https://drive.google.com/file/d/1cydk2eOr9NbuABWeNr7SK2gW-jAUXeSN/view?usp=drive_link" style="color:#2E75B6">PARS İKA — KTR Dokümanı</a></p>"""
    return _html("PARS Takımı — TEKNOFEST 2026 | Sponsorluk Teklifi", icerik, gonderen_ad, takim_mail, yetkili, sirket)

SABLONLAR = {
    "savunma":   _savunma,
    "otomasyon": _otomasyon,
    "yazilim":   _yazilim,
    "imalat":    _imalat,
    "yayin":     _yayin,
    "gida":      _gida,
    "otel":      _otel,
    "ilac":      _ilac,
    "giyim":     _giyim,
    "elektronik":_elektronik,
    "otomotiv":  _otomotiv,
    "teknokent": _teknokent,
    "genel":     _genel,
}