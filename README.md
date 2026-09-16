# dovecot-mass-password-changer

Language: EN

`reset_dovecot_passwords.py` resets the passwords of **all** mail users listed in `/etc/dovecot/users`. It generates a rule-compliant random password for each user, hashes it, updates Dovecot's user file, and shows you the plaintext passwords.

## Password Rules

Every generated password follows these rules:

- **Length**: 12 characters
- **1st and 12th character**: letters only (upper or lower case), never a digit or symbol
- **Middle 10 characters**: a mix of uppercase, lowercase, digits, and these symbols: `+ - _ . * ? ! # $ &`
- Every password is guaranteed to contain **at least 1 uppercase** and **1 lowercase** letter

Example: `Kj4#mPq9*wZ` *(actual generated passwords will be random)*

## Prerequisites

- The script must be run as **root** (`sudo`)
- `doveadm` must be installed on the server (comes bundled with Dovecot, no extra install normally needed)
- `/etc/dovecot/users` must exist and be in the correct format (`email@domain.com:{HASH}...`)

## Usage

```bash
sudo python3 reset_dovecot_passwords.py
```

When run, the script will:

1. List every user found in `/etc/dovecot/users` and print them to the screen
2. Ask for confirmation before proceeding — type `yes` and press Enter to continue
3. Back up `/etc/dovecot/users` (suffixed with `.bak-TIMESTAMP`, in the same folder)
4. Generate a new password for each user and hash it with `doveadm pw -s SHA512-CRYPT`
5. Update `/etc/dovecot/users` with the new hashes
6. Print the plaintext passwords **to the screen** and also save them to `/root/new_mail_passwords_TIMESTAMP.txt`
7. Restart the Dovecot service

## After Running

### 1. Move the passwords somewhere safe

Immediately copy the passwords shown on screen and in `/root/new_mail_passwords_TIMESTAMP.txt` into a password manager (1Password, Bitwarden, etc.) or another secure note system.

### 2. Delete the plaintext file from the server

Once the passwords are safely stored elsewhere, permanently delete the plaintext file from the server:

```bash
sudo shred -u /root/new_mail_passwords_TIMESTAMP.txt
```

(replace `TIMESTAMP` with the actual timestamp shown in the script's output)

### 3. Update mail clients (Thunderbird, iPhone Mail, etc.)

After the script runs, **every user's old password stops working**. You'll need to enter the new password on every device, for every account — otherwise those devices will fail to send/receive mail.

## Troubleshooting

**Script fails with "doveadm command not found":**
Confirm Dovecot is installed:
```bash
which doveadm
```
If empty, install it with `sudo apt install dovecot-core`.

**A user's password isn't working:**
Check that the corresponding line in `/etc/dovecot/users` is correctly formatted:
```bash
grep "user@domain.com" /etc/dovecot/users
```
The line should look like `email:{SHA512-CRYPT}$6$...`. If something looks off, restart Dovecot:
```bash
sudo systemctl restart dovecot
```

**I need to roll back to the old passwords:**
Restore the backup the script created:
```bash
sudo cp /etc/dovecot/users.bak-TIMESTAMP /etc/dovecot/users
sudo systemctl restart dovecot
```

## Security Notes

- The plaintext password file is created with **root-only read permissions** (`600`), but you should still delete it once you're done with it.
- The backup file (`.bak-TIMESTAMP`) contains old password *hashes* (not plaintext), but it's still good practice to clean these up after a while:
  ```bash
  sudo rm /etc/dovecot/users.bak-*
  ```
- This script resets **all** existing users' passwords — it does not target specific users. If you only want to reset one user's password, it's more appropriate to run `doveadm pw -s SHA512-CRYPT` manually and update that one line yourself.

---

---

# dovecot-mass-password-changer

Dil: TR

`reset_dovecot_passwords.py`, `/etc/dovecot/users` dosyasındaki **tüm mail kullanıcılarının** şifresini toplu olarak yeniler. Her kullanıcı için kurallara uygun rastgele bir şifre üretir, hash'ler, Dovecot'un kullanıcı dosyasını günceller ve düz metin şifreleri size gösterir.

## Şifre Kuralları

Üretilen her şifre şu kurallara uyar:

- **Uzunluk**: 12 karakter
- **1. ve 12. karakter**: sadece harf (büyük veya küçük), rakam/sembol olamaz
- **Ortadaki 10 karakter**: büyük harf + küçük harf + rakam + şu semboller: `+ - _ . * ? ! # $ &`
- Her şifrede **en az 1 büyük harf** ve **en az 1 küçük harf** garanti edilir

Örnek: `Kj4#mPq9*wZ` *(gerçek üretilen şifreler rastgele olacaktır)*

## Ön Koşullar

- Script **root olarak** çalıştırılmalı (`sudo`)
- `doveadm` komutu sunucuda kurulu olmalı (Dovecot paketiyle birlikte gelir, normalde ek kurulum gerekmez)
- `/etc/dovecot/users` dosyası mevcut ve doğru formatta olmalı (`email@domain.com:{HASH}...`)

## Kullanım

```bash
sudo python3 reset_dovecot_passwords.py
```

Script çalıştığında:

1. `/etc/dovecot/users` dosyasındaki tüm kullanıcıları listeler ve ekrana yazar
2. Devam etmeden önce onay ister — sadece `yes` yazıp Enter'a basarsanız işlem başlar
3. `/etc/dovecot/users` dosyasının yedeğini alır (`.bak-TARIH` uzantısıyla, aynı klasörde)
4. Her kullanıcı için yeni bir şifre üretir ve `doveadm pw -s SHA512-CRYPT` ile hash'ler
5. `/etc/dovecot/users` dosyasını yeni hash'lerle günceller
6. Düz metin şifreleri **ekrana yazdırır** ve `/root/new_mail_passwords_TARIH.txt` dosyasına kaydeder
7. Dovecot servisini yeniden başlatır

## Çalıştırma Sonrası Yapılması Gerekenler

### 1. Şifreleri güvenli bir yere taşıyın

Ekranda ve `/root/new_mail_passwords_TARIH.txt` dosyasında görünen şifreleri **hemen** bir şifre yöneticisine (1Password, Bitwarden vb.) veya güvenli bir not sistemine kaydedin.

### 2. Sunucudaki düz metin dosyasını silin

Şifreleri güvenli yere taşıdıktan sonra, sunucuda düz metin olarak duran dosyayı kalıcı olarak silin:

```bash
sudo shred -u /root/new_mail_passwords_TARIH.txt
```

(`TARIH` kısmını script çıktısında gösterilen gerçek tarih/saat damgasıyla değiştirin)

### 3. Mail istemcilerini (Thunderbird, iPhone Mail vb.) güncelleyin

Script çalıştıktan sonra **tüm kullanıcıların eski şifresi geçersiz olur**. Her cihazda, her hesap için yeni şifreyi girmeniz gerekir — aksi halde o cihazlar mail gönderemez/alamaz.

## Sorun Giderme

**Script "doveadm komutunu bulamadı" hatası veriyor:**
Dovecot'un kurulu olduğunu doğrulayın:
```bash
which doveadm
```
Boş dönerse `sudo apt install dovecot-core` ile kurun.

**Bir hesabın şifresi çalışmıyor:**
`/etc/dovecot/users` dosyasında ilgili satırın doğru formatta olduğunu kontrol edin:
```bash
grep "kullanici@domain.com" /etc/dovecot/users
```
Satır `email:{SHA512-CRYPT}$6$...` formatında olmalı. Sorun varsa Dovecot'u yeniden başlatın:
```bash
sudo systemctl restart dovecot
```

**Eski şifrelere geri dönmem gerekiyor:**
Script'in aldığı yedeği geri yükleyin:
```bash
sudo cp /etc/dovecot/users.bak-TARIH /etc/dovecot/users
sudo systemctl restart dovecot
```

## Güvenlik Notları

- Script'in ürettiği düz metin şifre dosyası **sadece root tarafından okunabilir** izinle (`600`) oluşturulur, ama yine de dosyayı işiniz bittiğinde silmeniz önerilir.
- Yedek dosyası (`.bak-TARIH`) de eski hash'leri içerir (düz metin şifre değil), ama gerekmiyorsa bir süre sonra temizlemekte fayda var:
  ```bash
  sudo rm /etc/dovecot/users.bak-*
  ```
- Bu script **mevcut tüm kullanıcıların** şifresini değiştirir — sadece belirli kullanıcıları hedeflemez. Belirli bir kullanıcının şifresini değiştirmek isterseniz `doveadm pw -s SHA512-CRYPT` komutunu elle çalıştırıp ilgili satırı manuel güncellemeniz daha uygun olur.
