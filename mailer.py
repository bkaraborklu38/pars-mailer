"""
PARS Takımı — Otomatik Sponsorluk Mailer
=========================================
Nasıl çalışır:
  1. Sheets'teki "Üyeler" sekmesinden isim→mail eşlemesini okur
  2. Her üye sekmesini tarar, "Hazır" + mail adresi dolu satırları seçer
  3. O üyenin adı ve mailiniden Brevo SMTP ile gönderir
  4. Gönderilenlerin durumunu "Gönderildi" yapar, tarih yazar
  5. Günlük limit dolunca durur

Kullanım:
  python mailer.py                    → Normal çalıştır
  python mailer.py --dry-run          → Mail atmadan test et
  python mailer.py --limit 10         → Sadece 10 mail gönder
  python mailer.py --uye BERAT        → Sadece belirli üyeyi çalıştır
"""

import os, time, random, argparse, smtplib, logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from templates import get_template
from assets import SPONSORLUK_B64
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("mailer.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# ── Sabit ayarlar ─────────────────────────────────────────────────
BREVO_SMTP_HOST   = "smtp-relay.brevo.com"
BREVO_SMTP_PORT   = 587
BREVO_SMTP_USER   = os.getenv("BREVO_SMTP_USER")
BREVO_API_KEY     = os.getenv("BREVO_API_KEY")
SHEETS_ID         = os.getenv("SHEETS_ID")
SERVICE_ACCT_FILE = os.getenv("SERVICE_ACCT_FILE", "service_account.json")
TAKIM_MAIL        = os.getenv("TAKIM_MAIL", "teampars.info@gmail.com")
GUNLUK_LIMIT      = int(os.getenv("GUNLUK_LIMIT", "60"))
BEKLEME_MIN_SN    = int(os.getenv("BEKLEME_MIN_SN", "180"))
BEKLEME_MAX_SN    = int(os.getenv("BEKLEME_MAX_SN", "420"))

# Sekme adı → tam isim eşlemesi (küçük harfe çevrilmiş key)
UYE_ISIMLER = {
    "mahmut":          "Mahmut Tosun",
    "enes":            "Müslüm Enes Culban",
    "ibrahim":         "İbrahim Avcı",
    "ibrahim muhammed":"İbrahim Muhammed Karaca",
    "said":            "Said Çifci",
    "selin":           "Selin Yılar",
    "melih":           "Melih Güner",
    "merve":           "Merve Gül Yıldız",
    "yaren":           "Yaren Azra Yaşar",
    "gülsüm":          "Ümmügülsüm Ökdem",
    "berat":           "Berat Karabörklü",
    "kağan":           "Buğra Kağan Balcı",
    "şehnaz":          "Şehnaz Ece Yapıcı",
}

# Üye adı → Gmail alias (Reply-To için)
UYE_ALIAS = {
    "Berat Karabörklü":       "teampars.info+berat@gmail.com",
    "Buğra Kağan Balcı":      "teampars.info+kagan@gmail.com",
    "İbrahim Avcı":           "teampars.info+ibrahim@gmail.com",
    "İbrahim Muhammed Karaca":"teampars.info+ibrahimmuhammed@gmail.com",
    "Mahmut Tosun":           "teampars.info+mahmut@gmail.com",
    "Merve Gül Yıldız":       "teampars.info+merve@gmail.com",
    "Müslüm Enes Culban":     "teampars.info+enes@gmail.com",
    "Said Çifci":             "teampars.info+said@gmail.com",
    "Selin Yılar":            "teampars.info+selin@gmail.com",
    "Şehnaz Ece Yapıcı":      "teampars.info+sehnaz@gmail.com",
    "Ümmügülsüm Ökdem":       "teampars.info+gülsüm@gmail.com",
    "Yaren Azra Yaşar":       "teampars.info+yaren@gmail.com",
    "Melih Güner":            "teampars.info+melih@gmail.com",
}

# Üye adı → PDF numarası (alfabetik sıra)
UYE_NO = {
    "Berat Karabörklü":       "00",
    "Buğra Kağan Balcı":      "01",
    "İbrahim Avcı":           "02",
    "İbrahim Muhammed Karaca":"03",
    "Mahmut Tosun":           "04",
    "Merve Gül Yıldız":       "05",
    "Müslüm Enes Culban":     "06",
    "Said Çifci":             "07",
    "Selin Yılar":            "08",
    "Şehnaz Ece Yapıcı":      "09",
    "Ümmügülsüm Ökdem":       "10",
    "Yaren Azra Yaşar":       "11",
    "Melih Güner":            "12",
}

def sekme_adi_to_isim(sekme_adi: str) -> str:
    """Sekme adından gönderici ismini döndürür. Türkçe karakter duyarsız."""
    arama = sekme_adi.strip().lower().replace("i̇", "i").replace("İ".lower(), "i")
    # Türkçe büyük İ → i dönüşümü
    arama = ""
    for c in sekme_adi.strip():
        if c == "İ":
            arama += "i"
        elif c == "I":
            arama += "ı"
        else:
            arama += c.lower()
    return UYE_ISIMLER.get(arama, sekme_adi.strip())

# Sütun indeksleri (0'dan) — v3 yapısı
# A=0(boş), B=1(#), C=2(Şirket), D=3(Mail), E=4(Sektör), F=5(Durum), G=6(ÖzelNot), H=7(Tarih)
COL_SIRKET   = 2
COL_MAIL     = 3
COL_SEKTOR   = 4
COL_DURUM    = 5
COL_OZEL_NOT = 6
COL_TARIH    = 7

DURUM_HAZIR      = "Hazır"
DURUM_GONDERILDI = "Gönderildi"

# Atlanacak sekmeler
ATLANAN_SEKMELER = {"özet", "taslak", "summary", "mail", "üyeler", "members"}

# ── Google Sheets bağlantısı ──────────────────────────────────────
def sheets_baglan():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(SERVICE_ACCT_FILE, scopes=scopes)
    gc    = gspread.authorize(creds)
    sh    = gc.open_by_key(SHEETS_ID)
    log.info(f"Sheets bağlandı: {sh.title}")
    return sh



# ── Hazır satırları getir ─────────────────────────────────────────
def hazir_satirlar(sheet) -> list:
    tum = sheet.get_all_values()
    sonuc = []
    for i, row in enumerate(tum):
        if i == 0:
            continue
        while len(row) < 8:
            row.append("")
        mail   = row[COL_MAIL].strip()
        durum  = row[COL_DURUM].strip()
        sirket = row[COL_SIRKET].strip()
        if mail and durum.strip().lower() == DURUM_HAZIR.lower() and sirket:
            sonuc.append({
                "row_idx":  i + 1,
                "sirket":   sirket,
                "mail":     mail,
                "sektor":   row[COL_SEKTOR].strip(),
                "ozel_not": row[COL_OZEL_NOT].strip(),
                "sekme":    sheet.title,
            })
    return sonuc

# ── Mail şablonu ──────────────────────────────────────────────────
def mail_olustur(kayit: dict, gonderen_ad: str) -> tuple[str, str]:
    return get_template(
        kategori    = kayit.get("sektor", ""),
        sirket      = kayit["sirket"],
        yetkili     = "",
        ozel_not    = "",
        gonderen_ad = gonderen_ad,
        takim_mail  = TAKIM_MAIL,
    )

# ── Mail gönder ───────────────────────────────────────────────────
def mail_gonder(kayit: dict, gonderen_ad: str, gonderen_mail: str,
                dry_run: bool = False) -> bool:
    konu, govde = mail_olustur(kayit, gonderen_ad)
    if dry_run:
        log.info(f"[DRY-RUN] {gonderen_ad} → {kayit['mail']} | {kayit['sirket']}")
        return True
    try:
        msg = MIMEMultipart("mixed")
        msg["Subject"] = konu
        msg["From"]    = f"{gonderen_ad} <{gonderen_mail}>"
        msg["To"]      = kayit["mail"]
        msg["Reply-To"]= UYE_ALIAS.get(gonderen_ad, gonderen_mail)
        # Brevo etiketleme — dashboard'da takip için
        msg["X-Mailin-Tag"]      = f"TEKNOFEST-SPONSORLUK,{kayit['sekme']},{kayit.get('sektor','genel')}"
        msg["X-Mailin-Campaign"] = "PARS-IKA-2026"
        # Gmail filtresi için gizli header — alıcı görmez
        msg["X-PARS-Gonderen"]   = gonderen_ad.split()[0]

        # HTML gövde
        html_part = MIMEMultipart("alternative")
        html_part.attach(MIMEText(govde, "html", "utf-8"))
        msg.attach(html_part)

        # Sponsorluk PDF eki
        import base64 as _b64
        from email.mime.application import MIMEApplication
        pdf_data = _b64.b64decode(SPONSORLUK_B64)
        pdf_part = MIMEApplication(pdf_data, _subtype="pdf")
        pdf_part.add_header("Content-Disposition", "attachment",
                            filename="PARS_IKA_Sponsorluk_Belgesi.pdf")
        msg.attach(pdf_part)

        with smtplib.SMTP(BREVO_SMTP_HOST, BREVO_SMTP_PORT) as server:
            server.starttls()
            server.login(BREVO_SMTP_USER, BREVO_API_KEY)
            server.sendmail(gonderen_mail, kayit["mail"], msg.as_string())

        log.info(f"✓ {gonderen_ad} → {kayit['mail']} | {kayit['sirket']}")

        # Gmail SMTP ile takım mailine kopya gönder — Gönderildi klasörüne düşer
        try:
            gmail_pass = os.getenv("GMAIL_APP_PASSWORD", "")
            if gmail_pass:
                kopya = MIMEMultipart("mixed")
                # İsim eşleşmesini normalize ederek yap
                no = "99"
                for isim, numara in UYE_NO.items():
                    if isim.lower().strip() == gonderen_ad.lower().strip():
                        no = numara
                        break
                if no == "99":
                    log.warning(f"UYE_NO eşleşmedi: '{gonderen_ad}' (bytes: {gonderen_ad.encode()})")
                kopya["Subject"] = f"[KOPYA][{no}] {konu}"
                kopya["From"]    = f"{gonderen_ad} <{TAKIM_MAIL}>"
                kopya["To"]      = TAKIM_MAIL
                kopya.attach(MIMEText(govde, "html", "utf-8"))
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as gm:
                    gm.login(TAKIM_MAIL, gmail_pass)
                    gm.sendmail(TAKIM_MAIL, TAKIM_MAIL, kopya.as_string())
                log.info("  → Gmail Gönderildi klasörüne kopyalandı")
        except Exception as gmail_err:
            log.warning(f"  → Gmail kopyalama başarısız: {gmail_err}")

        return True
    except Exception as e:
        log.error(f"✗ Hata → {kayit['mail']} | {e}")
        return False

# ── Sheets güncelle ───────────────────────────────────────────────
def durum_guncelle(sheet, row_idx: int, durum: str = "gonderildi", dry_run: bool = False):
    if dry_run:
        return
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
    if durum == "gonderildi":
        sheet.update_cell(row_idx, COL_DURUM + 1, DURUM_GONDERILDI)
        sheet.update_cell(row_idx, COL_TARIH + 1, tarih)
        # Satırı yeşile boya
        yesil = {"backgroundColor": {"red": 0.85, "green": 0.96, "blue": 0.85}}
        try:
            sheet.spreadsheet.batch_update({"requests": [{"repeatCell": {
                "range": {"sheetId": sheet.id, "startRowIndex": row_idx-1, "endRowIndex": row_idx, "startColumnIndex": 1, "endColumnIndex": 8},
                "cell": {"userEnteredFormat": {"backgroundColor": {"red": 0.85, "green": 0.96, "blue": 0.85}}},
                "fields": "userEnteredFormat.backgroundColor"
            }}]})
        except: pass
    elif durum == "hata":
        sheet.update_cell(row_idx, COL_DURUM + 1, "Hata")
        sheet.update_cell(row_idx, COL_TARIH + 1, tarih)
        # Satırı kırmızıya boya
        try:
            sheet.spreadsheet.batch_update({"requests": [{"repeatCell": {
                "range": {"sheetId": sheet.id, "startRowIndex": row_idx-1, "endRowIndex": row_idx, "startColumnIndex": 1, "endColumnIndex": 8},
                "cell": {"userEnteredFormat": {"backgroundColor": {"red": 0.96, "green": 0.85, "blue": 0.85}}},
                "fields": "userEnteredFormat.backgroundColor"
            }}]})
        except: pass

# ── Ana döngü ─────────────────────────────────────────────────────
def calistir(dry_run=False, limit=None, sadece_uye=None):
    efektif_limit = limit or GUNLUK_LIMIT
    log.info(f"=== PARS Mailer | limit={efektif_limit} | dry_run={dry_run} | uye={sadece_uye or 'hepsi'} ===")
##
    sh         = sheets_baglan()
    gonderilen = 0
    atlanan    = 0

    for sekme in sh.worksheets():
        if gonderilen >= efektif_limit:
            log.info(f"Limit doldu ({efektif_limit}), duruluyor.")
            break

        baslik = sekme.title.strip()

        # Sistem sekmelerini atla
        if baslik.lower() in ATLANAN_SEKMELER:
            continue

        # Belirli üye filtresi
        if sadece_uye and baslik.lower() != sadece_uye.lower():
            continue

        # Sekme adından gönderici ismini bul, mail hep takım maili
        gonderen_ad   = sekme_adi_to_isim(baslik)
        gonderen_mail = TAKIM_MAIL

        log.info(f"--- {baslik} → gönderici: {gonderen_ad} ---")
        kayitlar = hazir_satirlar(sekme)
        log.info(f"  Hazır: {len(kayitlar)} kayıt")

        for k in kayitlar:
            if gonderilen >= efektif_limit:
                break

            ok = mail_gonder(k, gonderen_ad, gonderen_mail, dry_run=dry_run)
            if ok:
                durum_guncelle(sekme, k["row_idx"], durum="gonderildi", dry_run=dry_run)
                gonderilen += 1
                if gonderilen < efektif_limit:
                    bekleme = random.randint(BEKLEME_MIN_SN, BEKLEME_MAX_SN)
                    log.info(f"  Bekleniyor: {bekleme}s ({bekleme//60}:{bekleme%60:02d} dk)")
                    time.sleep(bekleme)
            else:
                durum_guncelle(sekme, k["row_idx"], durum="hata", dry_run=dry_run)
                atlanan += 1

    log.info(f"=== Bitti | Gönderilen: {gonderilen} | Hatalı: {atlanan} ===")

# ── CLI ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PARS Sponsorluk Mailer")
    parser.add_argument("--dry-run", action="store_true", help="Mail atmadan test et")
    parser.add_argument("--limit",   type=int, default=None, help="Bu çalışmadaki limit")
    parser.add_argument("--uye",     type=str, default=None, help="Sadece bu üyeyi çalıştır (örn: BERAT)")
    args = parser.parse_args()
    calistir(dry_run=args.dry_run, limit=args.limit, sadece_uye=args.uye)
