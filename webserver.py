import sys, signal
import http.server
import socketserver

# Se c'è un argomento nella riga di comando, viene usato come porta. Altrimenti, viene usata la porta 8080.
if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = 8080

# Crea un server TCP che gestisce più richieste simultaneamente usando i thread.
server = socketserver.ThreadingTCPServer(('', port), http.server.SimpleHTTPRequestHandler)
print(f"Il server HTTP verrà eseguito all\'indirizzo http://localhost:{port}/")

# Configura il server per usare thread daemon e permettere il riutilizzo dell'indirizzo.
server.daemon_threads = True  
server.allow_reuse_address = True  

# Definisce una funzione per gestire il segnale di interruzione (Ctrl+C).
def signal_handler(signal, frame):
    print('Uscita dal server HTTP (premuto Ctrl+C)')
    try:
        if server:
            server.server_close()  # Chiude il server se è attivo.
    finally:
        sys.exit(0)  # Esce dal programma.

# Associa il segnale SIGINT (interruzione, ad esempio, Ctrl+C) alla funzione signal_handler.
signal.signal(signal.SIGINT, signal_handler)

# Tenta di eseguire il server indefinitamente.
try:
    while True:
        server.serve_forever()  # Mantiene il server in esecuzione.
except KeyboardInterrupt:
    pass  # Cattura l'eccezione di interruzione della tastiera (Ctrl+C).

# Chiude il server all'uscita dal ciclo.
server.server_close()
