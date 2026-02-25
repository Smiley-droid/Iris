import os
import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser  # Pour ouvrir des sites
import requests    # Pour API météo
import random      # Pour blagues aléatoires

# charge les variables d'environnement depuis .env (nécessite python-dotenv)
from dotenv import load_dotenv
load_dotenv()

# Initialisation du moteur de parole
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Vitesse de parole
engine.setProperty('volume', 1.0)  # Volume max
# Pour une voix française, décommente et ajuste si besoin :
# voices = engine.getProperty('voices')
# for voice in voices:
#     if 'french' in voice.name.lower():
#         engine.setProperty('voice', voice.id)
#         break

print("🎤 Programme lancé → Je t'écoute en permanence !")
print("Parle quand tu veux, je suis là... (dis 'arrête' pour quitter)")

r = sr.Recognizer()
with sr.Microphone() as source:
    print("✅ Micro calibré ! Go !")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="fr-FR")
            print(f"👂 Tu as dit : {text}")
            text_lower = text.lower()

            if "arrête" in text_lower:
                engine.say("Au revoir, à bientôt !")
                engine.runAndWait()
                break

            elif "heure" in text_lower:
                now = datetime.now().strftime("%H:%M")
                response = f"Il est {now.replace(':', ' heures ')} minutes."
                print(f"🕒 {response}")
                engine.say(response)
                engine.runAndWait()

            elif "bonjour" in text_lower:
                response = "Salut toi ! Ça va bien ? Dis-moi ce que je peux faire pour toi."
                print(f"🤖 {response}")
                engine.say(response)
                engine.runAndWait()

            # Ouvre un site web
            elif "ouvre" in text_lower and "site" in text_lower:
                site = text_lower.split("ouvre ")[-1].replace("site", "").strip()  # Ex: "ouvre google"
                url = f"https://www.{site}.com"
                webbrowser.open(url)
                response = f"J'ouvre le site {site} pour toi !"
                print(f"🌐 {response}")
                engine.say(response)
                engine.runAndWait()

            # Raconte une blague
            elif "blague" in text_lower:
                blagues = [
                    "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau !",
                    "Qu'est-ce qu'un citron qui se jette à l'eau ? Un citron pressé !",
                    "Pourquoi les oiseaux ne portent-ils pas de lunettes ? Parce qu'ils ont des lentilles de contact !"
                ]
                blague = random.choice(blagues)
                response = blague
                print(f"😂 {response}")
                engine.say(response)
                engine.runAndWait()

            elif "météo" in text_lower or "temps":
                ville = text_lower.split("météo ")[-1].strip() or "Paris"  # Défaut à Paris
                api_key = os.getenv("API_KEY_METEO")  # récupérée depuis .env
                url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric&lang=fr"
                try:
                    data = requests.get(url).json()
                    if data["cod"] == 200:
                        temp = data["main"]["temp"]
                        desc = data["weather"][0]["description"]
                        response = f"À {ville}, il fait {temp} degrés avec {desc}."
                    else:
                        response = "Désolé, je n'ai pas pu trouver la météo pour cette ville."
                except:
                    response = "Problème avec la connexion pour la météo."
                print(f"☁️ {response}")
                engine.say(response)
                engine.runAndWait()

            # Recherche web simple
            elif "cherche" in text_lower:
                query = text_lower.split("cherche ")[-1].strip()
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                response = f"Je lance une recherche pour {query} !"
                print(f"🔍 {response}")
                engine.say(response)
                engine.runAndWait()

            else:
                response = "Désolé, je n'ai pas compris cette commande. Essaie autre chose !"
                print(f"❓ {response}")
                engine.say(response)
                engine.runAndWait()

        except sr.UnknownValueError:
            print("Désolé, je n'ai pas compris...")
        except sr.RequestError:
            print("Problème avec le service de reconnaissance...")
