#!/usr/bin/env python3

import subprocess
import random
import string
import sys
import os
import shutil
from datetime import datetime

DOVECOT_USERS_FILE = "/etc/dovecot/users"
ALLOWED_SYMBOLS = "+-_.*?!#$&"
PASSWORD_LENGTH = 12


def generate_password():
    letters = string.ascii_letters  # a-zA-Z
    middle_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + ALLOWED_SYMBOLS

    while True:
        first_char = random.choice(letters)
        last_char = random.choice(letters)
        middle_chars = [random.choice(middle_charset) for _ in range(PASSWORD_LENGTH - 2)]

        password_chars = [first_char] + middle_chars + [last_char]
        password = "".join(password_chars)

        has_upper = any(c in string.ascii_uppercase for c in password)
        has_lower = any(c in string.ascii_lowercase for c in password)

        if password[0] not in letters or password[-1] not in letters:
            continue

        if has_upper and has_lower:
            return password


def hash_password(plain_password):
    result = subprocess.run(
        ["doveadm", "pw", "-s", "SHA512-CRYPT", "-p", plain_password],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def read_users(filepath):
    emails = []
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        sys.exit(1)

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            email = line.split(":", 1)[0]
            if email:
                emails.append(email)
    return emails


def main():
    if os.geteuid() != 0:
        print("This script must run by root (use sudo).")
        sys.exit(1)

    emails = read_users(DOVECOT_USERS_FILE)
    if not emails:
        print("No user found, quiting.")
        sys.exit(1)

    print(f"{len(emails)} users found:")
    for e in emails:
        print(f"  - {e}")
    print()

    confirm = input("Should the password be reset for ALL of these users? (type yes); ")
    if confirm.strip().lower() != "yes":
        print("Process canceled.")
        sys.exit(0)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = f"{DOVECOT_USERS_FILE}.bak-{timestamp}"
    shutil.copy2(DOVECOT_USERS_FILE, backup_path)
    print(f"Backup: {backup_path}")

    results = []  # (email, plain_password)
    new_lines = []

    for email in emails:
        plain_password = generate_password()
        hashed = hash_password(plain_password)
        new_lines.append(f"{email}:{hashed}")
        results.append((email, plain_password))
        print(f"OK: {email} -> new password generated")

    with open(DOVECOT_USERS_FILE, "w") as f:
        f.write("\n".join(new_lines) + "\n")

    print(f"\n{DOVECOT_USERS_FILE} updated.")

    output_path = f"/root/new_mail_passwords_{timestamp}.txt"
    with open(output_path, "w") as f:
        f.write(f"New mail passwords - {timestamp}\n")
        f.write("=" * 50 + "\n\n")
        for email, pw in results:
            f.write(f"{email} : {pw}\n")

    os.chmod(output_path, 0o600)

    print("\n" + "=" * 50)
    print("NEW PASSWORDS (plaintext) - SAVE TO SECURE PLACE:")
    print("=" * 50)
    for email, pw in results:
        print(f"{email} : {pw}")
    print("=" * 50)
    print(f"\nThis list was also written to the following file: {output_path}")
    print("IMPORTANT: It is recommended to delete this file from the server after noting it down:")
    print(f"  sudo shred -u {output_path}")

    print("\nDovecot restarting...")
    subprocess.run(["systemctl", "restart", "dovecot"], check=True)
    print("Dovecot restarted. Process OK.")


if __name__ == "__main__":
    main()
