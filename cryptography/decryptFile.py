from cryptography.fernet import Fernet

key = "ZKG-hah0-GiBfJOqhwbzobPEvh9z1xhFOPYIimr5Id4="

e_keys = "e_key_log.txt"
e_sys_info = "e_sysInfo.txt"
e_clipboard_info = "e_clipboard.txt"

encrypted_files = [e_keys, e_sys_info, e_clipboard_info]

file_count = 0

for file in encrypted_files:

    with open(encrypted_files[file_count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open(encrypted_files[file_count], 'wb') as f:
        f.write(decrypted)
    
    file_count += 1