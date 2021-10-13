import socket
import threading

# Constantes
HOST = '127.0.0.1'
PORT = 3001
FORMAT = 'utf8'
# Constantes


# Initialisation
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
clients, pseudos = [], []


# Initialisation
# Methode pour demmarer le serveur
def startChat():
    print(f"Serveur démmaré sur {HOST}:{PORT}")
    server.listen()
    while True:
        conn, addr = server.accept()
        connected = False
        while not connected:
            conn.send("PSEUDO".encode(FORMAT))
            pseudo = conn.recv(1024).decode(FORMAT)
            if pseudo.lower() in pseudos:
                connected = False
                conn.send("USED".encode(FORMAT))
            else:
                pseudos.append(pseudo)
                with open("assets/fichiers/pseudos.txt", "r+") as fil:
                    pseus = fil.readlines()
                    if pseudo + "\n" not in pseus:
                        fic = open("assets/fichiers/pseudos.txt", "a+")
                        fic.write(pseudo + "\n")
                        fic.close()
                    fil.close()
                clients.append(conn)
                connected = True

        print(f"{pseudo} s'est connecté")
        # Message diffusé à tous les clients connectés
        diffusionMessage(f"\t\t\t{pseudo} a rejoint le chat!!!".encode(FORMAT))
        # Thread pour l'attente de message
        thread = threading.Thread(target=handle, args=(conn, addr))
        thread.start()

        # Affiche le nombre de clients connectés
        print(f"Nombre de connecté(s) {threading.activeCount() - 1}")


# Méthode pour le thread de chaque client
def handle(conn, addr):
    print(f"Nouvelle connexion avec {addr}")
    connected = True
    while connected:
        message = conn.recv(1024)
        diffusionMessage(message)
        with open("assets/fichiers/messages.txt", "a+") as fic:
            if message.decode(FORMAT):
                fic.write(message.decode(FORMAT) + '\n')
                fic.close()
    conn.close()


# Methode de duffusion de message pour tous les clients connectés
def diffusionMessage(message):
    for client in clients:
        client.send(message)


# Démamarage du serveur
startChat()
