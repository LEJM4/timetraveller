import subprocess as supr

def installieren_aller_requirements():
    try:
        #installieren aller anderen requirements
        #pygame
        supr.run(['pip', 'install', 'pygame-ce'], shell=True, check=True) 
        #pytmx
        supr.run(['pip', 'install', 'pytmx'], shell=True, check=True) 

    
    except supr.CalledProcessError as error:
        print("Fehler bei der Installation: ", error)
        print("")
        print("Bitte führe den Code nochmal aus oder lade dir manuell 'pygame' und 'pytmx' herunter")
        print("Öffne 'cmd' und gib den Befehl 'pip install pygame' und danach 'pip install pytmx' ein.")
        print("")
        print("Dann führe den Code nocheinmal aus.")

    finally:
        #abschluss
        print("")
        print("Installation abgeschlossen.")

installieren_aller_requirements()