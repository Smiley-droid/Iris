import speech_recognition as sr
import pyttsx3
from datetime import datetime
import webbrowser
import requests
import random

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

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

            elif "ouvre" in text_lower and "site" in text_lower:
                site = text_lower.split("ouvre ")[-1].replace("site", "").strip()
                url = f"https://www.{site}.com"
                webbrowser.open(url)
                response = f"J'ouvre le site {site} pour toi !"
                print(f"🌐 {response}")
                engine.say(response)
                engine.runAndWait()

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

            elif "météo" in text_lower:
                ville = text_lower.split("météo ")[-1].strip() or "Paris"  # Défaut à Paris
                api_key = "TA_CLE_API"  # Mets ta clé ici !
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
