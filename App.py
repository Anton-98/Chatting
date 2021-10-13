import shutil
import socket
import threading
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import *

# Constantes
host = '127.0.0.1'
port = 3001
FORMAT = 'utf-8'
width = 720
height = 512
firstBg = "#276799"
secondBg = "#17b4ff"
textColor = "#ccfbef"
FONT = "Helvetica 28"
FONT_BOLD = "Helvetica 40 bold"
interdit = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "_")

# Constantes

# Initialisation

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


# Initialisation


class Chat:
    # fonction pour contrôler la saisie
    def validation(self, event):
        if not (122 >= event.keycode >= 97) and not (90 >= event.keycode >= 65) \
                and event.char != "@" and event.char not in interdit and event.keysym != "BackSpace" \
                and event.keysym != "Return" and event.keysym != "F2" and event.keysym != "F3" \
                and event.keysym != "F4" and event.keysym != "Down" and event.keysym != "Up" \
                and event.keysym != "Right" and event.keysym != "Left" and event.keysym != "Escape":
            if event.char:
                self.pseudoSaisi.delete(len(self.pseudoSaisi.get()) - 1, END)

    def passage(self, event):
        self.verifier(self.pseudoSaisi.get())

    def __init__(self):
        self.window = Tk()
        self.window.withdraw()
        self.login = Toplevel()
        self.login.title("Connexion")
        self.login.resizable(width=False, height=False)
        self.login.minsize(width, height)
        self.login.maxsize(width, height)
        self.img = Image("photo", file="assets/img/ico.png")
        self.login.tk.call("wm", 'iconphoto', self.login._w, self.img)
        self.login.configure(bg=firstBg)
        self.cadreCon = Frame(self.login, bg=secondBg)

        self.signIn = Label(self.cadreCon, text="CONNEXION", fg=textColor,
                            bg=secondBg, font=FONT_BOLD)
        self.signIn.grid(row=0, column=0, pady=50)

        self.cadrePseudo = Frame(self.cadreCon, bg=secondBg)

        self.pseudoLabel = Label(self.cadrePseudo, text="Pseudo", fg=textColor,
                                 bg=secondBg, font=FONT)
        self.pseudoSaisi = Entry(self.cadrePseudo, fg=textColor, border=3,
                                 highlightthickness=0, bg=secondBg, font=FONT)
        self.pseudoSaisi.config(highlightbackground=secondBg, highlightcolor=secondBg)
        self.pseudoSaisi.focus()
        self.pseudoSaisi.bind_all("<Key>", self.validation)
        self.pseudoSaisi.bind("<Return>", self.passage)
        self.cadrePseudo.grid(row=1, column=0, padx=50)
        self.pseudoLabel.grid(row=0, column=0, sticky=E, padx=25)
        self.pseudoSaisi.grid(row=0, column=2, sticky=E, ipadx=25)
        self.btnConnexion = Button(self.cadreCon, text='Se Connecter',
                                   width=15, relief="ridge", borderwidth=1,
                                   fg=secondBg, font=FONT, activeforeground=secondBg,
                                   cursor="hand2", activebackground=firstBg,
                                   command=lambda: self.verifier(self.pseudoSaisi.get()))
        self.btnConnexion.grid(row=2, column=0, pady=50)
        self.cadreCon.pack(expand=YES)
        self.window.mainloop()

    # Avant d'entrer dans le chat on doit respecter certaines régles pour les pseudos
    # A savoir le nombre de caratères, le pseudo ne commence pas par un chiffre ou un _
    # Et les pseudos ne doivent pas avoir des caratères spéciaux
    def verifier(self, pseudo):
        self.pseudo = pseudo
        if 8 >= len(pseudo) >= 3:
            if not pseudo.startswith(interdit):
                mess = client.recv(1024).decode(FORMAT)
                if mess == 'PSEUDO':
                    client.send(self.pseudo.encode(FORMAT))
                    mess2 = client.recv(1024).decode(FORMAT)
                    if mess2 == 'USED':
                        showinfo('Erreur', f'{self.pseudo} déja utilisé!!!')
                        self.pseudoSaisi.delete(0, END)
                    else:
                        self.login.destroy()
                        self.pseudoSaisi.unbind_all("<Key>")
                        self.pseudoSaisi.unbind_all("<Return>")
                        self.espaceClient(pseudo)
                        rec = threading.Thread(target=self.receive)
                        rec.start()
            else:
                showinfo('Erreur', 'Le pseudo ne doit pas commencer par un entier ou un _ !!!')
                self.pseudoSaisi.delete(0, END)
        else:
            showinfo('Erreur', 'Veuiller un pseudo qui a au moins 3 caractères et au plus 8 pour acceder au chat!!!')
            self.pseudoSaisi.delete(0, END)

    # Après avoir saisie l'utilisateur sera redirigé vers un espace qui lui permet de saisir des messages
    def espaceClient(self, pseudo):
        self.pseudo = pseudo
        self.window.deiconify()
        self.window.title("eChat")
        self.window.tk.call("wm", 'iconphoto', self.window._w, self.img)
        self.window.resizable(width=False, height=False)
        self.window.minsize(width, height)
        self.window.maxsize(width, height)
        self.window.configure(bg=firstBg)

        self.head = Label(self.window, bg=secondBg, fg=firstBg, text=self.pseudo, font=FONT, pady=5)
        self.head.place(relwidth=1)

        self.afficheMessage = Text(self.window, bg="#1978a5", fg="#031163",
                                   font="Helvetica 18", padx=15, pady=5)
        self.afficheMessage.place(relheight=0.78, relwidth=0.98, rely=0.11, relx=0.01)
        self.afficheMessage.config(state=DISABLED)
        self.scrollbarVertical = Scrollbar(self.afficheMessage)
        self.scrollbarVertical.place(relheight=1, relx=0.994)
        self.scrollbarVertical.config(command=self.afficheMessage.yview)

        self.messageEntre = Entry(self.window, bg=secondBg, fg=textColor, font=("Helvetica", 14))
        self.messageEntre.bind_all("<Return>", self.passe)
        self.messageEntre.place(relx=0.01, rely=0.99, anchor=SW, width=width - 137, height=35)
        self.messageEntre.focus()

        self.btnEnvoyer = Button(self.window, fg=firstBg,
                                 text="Envoyer", borderwidth=1.5,
                                 relief="ridge", font=("Helvetica", 20, "bold"),
                                 cursor="hand2", command=lambda: self.prepareEnvoie(self.messageEntre.get()))
        self.btnEnvoyer.place(relx=0.99, rely=0.99, anchor=SE, height=35, width=120)

        self.menubar = Menu(self.window)
        self.menu = Menu(self.menubar, tearoff=0)
        self.menu.add_command(label="Copier la liste des pseudos", command=self.charger)
        self.menu.add_command(label="Copier l'ensemble des messages", command=self.charger2)
        self.menu.add_command(label="Quitter", command=self.ferme_window)
        self.menubar.add_cascade(label="Fichier", menu=self.menu)
        self.window.config(menu=self.menubar)
        self.window.protocol("WM_DELETE_WINDOW", self.ferme_window)

    # Cette fonction permet de charger l'ensemble des pseudos qui se sont déjà connectées sur le chat
    def charger(self):
        self.dest = askdirectory()
        self.deste = self.dest + "/Pseudos.txt"
        self.src = "assets/fichiers/pseudos.txt"
        if shutil.copy(self.src, self.deste):
            showinfo('Message', f'Vous avez charger la liste des pseudos dans {self.deste}')

    # Cette fonction permet de charger l'ensemble des messages envoyés sur le chat
    def charger2(self):
        try:
            self.dest = askdirectory()
            self.deste = self.dest + "/Messages.txt"
            self.src = "assets/fichiers/messages.txt"
            if shutil.copy(self.src, self.deste):
                showinfo('Message', f'Vous avez charger l\'ensemble des messsages dans {self.deste}')
        except EXCEPTION:
            print(EXCEPTION)
            pass

    def passe(self, event):
        self.prepareEnvoie(self.messageEntre.get())

    # Permet de fermer et de quitter le chat
    def ferme_window(self):
        client.close()
        self.window.destroy()

    def prepareEnvoie(self, message):
        self.afficheMessage.config(state=DISABLED)
        self.message = message
        if message:
            self.messageEntre.delete(0, END)
            self.envoi = threading.Thread(target=self.envoie)
            self.envoi.start()

    def receive(self):
        with open("assets/fichiers/messages.txt", "r+") as fic:
            messages = fic.readlines()
            for mess in messages:
                msg = mess.split(' :')
                self.afficheMessage.config(state=NORMAL)
                if msg[0].lower() == self.pseudo.lower():
                    self.afficheMessage.insert(END, "Moi :" + msg[1] + "\n")
                else:
                    self.afficheMessage.insert(END, mess + "\n")

                self.afficheMessage.config(state=DISABLED)
                self.afficheMessage.see(END)
                fic.close()
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                msg = message.split(' :')
                # Si le serveur envoie le message PSEUDO le client lui retourne le pseudo saisi.

                # insertion du message dans la discussion
                self.afficheMessage.config(state=NORMAL)

                if msg[0] == self.pseudo:
                    self.afficheMessage.insert(END, "Moi :" + msg[1] + "\n\n")
                else:
                    self.afficheMessage.insert(END, message + "\n\n")
                self.afficheMessage.config(state=DISABLED)
                self.afficheMessage.see(END)
            except:
                # Erreur à afficher sur le console
                print("Une erreur est survenu lors de l'envoie du message contacter voter administrateur!")
                client.close()
                break

    def envoie(self):
        self.afficheMessage.config(state=DISABLED)
        while True:
            msg = f'{self.pseudo} : {self.message}'
            client.send(msg.encode(FORMAT))
            break


if __name__ == "__main__":
    App = Chat()
