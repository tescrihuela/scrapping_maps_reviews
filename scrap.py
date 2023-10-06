from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv
import time 

## Paramètres
class_div_commentaire = "jJc9Ad"
class_span_note = "fzvQIb"
class_span_commentaire = "wiI7pd"
class_span_date = "xRkPPb"
temps_attente = 6
nb_iterations = 10

## Inputs
endpoint_search = 'https://www.google.com/maps?output=search&q='
hotels =[
    {
        "nom":"hotel les arcades",
        "commune":"rouen"
    },
    {
        "nom":"Refuge de platé",
        "commune" : "passy"
    },
    {
    "nom" : "hotel celine",
    "commune": "Rouen"
    },
    {
    "nom" : "hotel ibis budget",
    "commune": "Le Petit Quevilly"
    }
]

# hotels = [
#     {   
#         "nom" : "Ehpad Saint Julien",
#         "url" : 'https://www.google.com/maps/place/H%C3%B4tel+Litt%C3%A9raire+Gustave+Flaubert,+BW+Signature+Collection/@49.4426077,1.0842829,17z/data=!4m11!3m10!1s0x47e0ddd8cbf056bb:0x302ec01a6d9fd1b2!5m2!4m1!1i2!8m2!3d49.4426077!4d1.0868578!9m1!1b1!16s%2Fg%2F1tg4_q96?entry=ttu'
#     },
#     {
#         "nom" : "Hôtel Ibis Budget Rouen",
#         "url" : 'https://www.google.com/maps/place/Hotel+ibis+budget+Rouen+Sud+Z%C3%A9nith/@49.3921363,1.0568755,17z/data=!4m22!1m10!3m9!1s0x47e0dfd774e03541:0x5b871dfdf5f9d066!2sHotel+ibis+budget+Rouen+Sud+Z%C3%A9nith!5m2!4m1!1i2!8m2!3d49.3921363!4d1.0594504!16s%2Fg%2F11_qhrys7!3m10!1s0x47e0dfd774e03541:0x5b871dfdf5f9d066!5m2!4m1!1i2!8m2!3d49.3921363!4d1.0594504!9m1!1b1!16s%2Fg%2F11_qhrys7?entry=ttu'
#     },
#     {
#         "nom" : "Hôtel Restaurant Campanile Rouen",
#         "url" : "https://www.google.com/maps/place/H%C3%B4tel+Restaurant+Campanile+Rouen+Z%C3%A9nith/@49.3904708,1.0467098,15z/data=!4m22!1m10!3m9!1s0x47e0dfd774e03541:0x5b871dfdf5f9d066!2sHotel+ibis+budget+Rouen+Sud+Z%C3%A9nith!5m2!4m1!1i2!8m2!3d49.3921363!4d1.0594504!16s%2Fg%2F11_qhrys7!3m10!1s0x47e0dfc5b3710a75:0xdbbdf698e40d981a!5m2!4m1!1i2!8m2!3d49.3906631!4d1.0595705!9m1!1b1!16s%2Fg%2F1thbvywt?entry=ttu"
#     },
#     {
#         "nom" : "Cosy Rouen", 
#         "url" : "https://www.google.com/maps/place/Cosy+Rouen/@49.4520342,1.0943715,15.21z/data=!4m22!1m10!3m9!1s0x47e0dfd774e03541:0x5b871dfdf5f9d066!2sHotel+ibis+budget+Rouen+Sud+Z%C3%A9nith!5m2!4m1!1i2!8m2!3d49.3921363!4d1.0594504!16s%2Fg%2F11_qhrys7!3m10!1s0x47e0ddceef095555:0x814683f14573fcdf!5m2!4m1!1i2!8m2!3d49.4549445!4d1.0959487!9m1!1b1!16s%2Fg%2F11f613czfh?entry=ttu"
#     },
#     {
#         "nom" : "Hôtel Céline", 
#         "url": "https://www.google.com/maps/place/H%C3%B4tel+C%C3%A9line/@49.4499697,1.0783211,15z/data=!4m22!1m10!3m9!1s0x47e0dfd774e03541:0x5b871dfdf5f9d066!2sHotel+ibis+budget+Rouen+Sud+Z%C3%A9nith!5m2!4m1!1i2!8m2!3d49.3921363!4d1.0594504!16s%2Fg%2F11_qhrys7!3m10!1s0x47e0ddd08e628fad:0x182b04dbc7b64a4c!5m2!4m1!1i2!8m2!3d49.4490763!4d1.0902084!9m1!1b1!16s%2Fg%2F1tfkkg8s?entry=ttu"
#     },
#     {
#         "nom" : "Hôtel Le vieux Carré",
#         "url" : "https://www.google.com/maps/place/H%C3%B4tel+Le+Vieux+Carr%C3%A9/@49.4429226,1.0995863,16.21z/data=!4m22!1m10!3m9!1s0x47e0dfd774e03541:0x5b871dfdf5f9d066!2sHotel+ibis+budget+Rouen+Sud+Z%C3%A9nith!5m2!4m1!1i2!8m2!3d49.3921363!4d1.0594504!16s%2Fg%2F11_qhrys7!3m10!1s0x47e0ddd7b2856b2f:0x70aee5bc43ce8950!5m2!4m1!1i2!8m2!3d49.4433516!4d1.0945895!9m1!1b1!16s%2Fg%2F1td29m6_?entry=ttu"
#     }
# ]


class Hotel():
    """"Classe Hotêl qui regarde si le mot 'punaise' est évoqué dans les premiers avis google de l'hôtel"""
    def __init__(self, url, nom = None):
        self.url = url
        self.nom = nom if nom else url
        self.nb_comm_punaise_de_lits = 0
        self.reviews = None
        self.get_reviews()

    def get_reviews(self):
        liste_avis = []

        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(self.url)

        # On passe la page de cookie
        driver.find_element(By.XPATH, "//span[contains(text(), 'Tout accepter')]").click()
        time.sleep(temps_attente)

        # On se rend dans les avis
        driver.find_element(By.XPATH, "//div[contains(text(), 'Avis')]").click()
        time.sleep(2)

        #on essaie de descendre 

        # On récupère les n premiers commentaires qui nous intéressent (chaque itération récupère 10 commentaires)
        for i in range(nb_iterations):    
            commentaires = driver.find_elements(By.XPATH, "//button[contains(text(), 'Plus')]") # cherche les boutons plus (= un commentaire)
            commentaires[-1].send_keys(Keys.END)    # appuie "fin de page" sur le dernier bouton "Plus"
            time.sleep(temps_attente)     # un peu d'attente (à augmenter si réseau trop lent pour charger les comm)
        [plus.click() for plus in driver.find_elements(By.XPATH, "//button[contains(text(), 'Plus')]")]     # on déplie tous les commentaires en cliquant sur le bouton "Plus"
        
        # On parse la page
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        for div_commentaire in soup.find_all("div", {"class": class_div_commentaire}):
            try:
                note= div_commentaire.find("span", {"class": class_span_note}).text
                commentaire = div_commentaire.find("span", {"class": class_span_commentaire}).text
                date = div_commentaire.find("span", {"class": class_span_date}).text
            except:
                note, commentaire, date = "", "", ""
                # commentaire = ""
            punaise = False
            if 'punaise' in commentaire.lower():
                punaise = True
                self.nb_comm_punaise_de_lits += 1

            liste_avis.append({"note" : note,"date": date, "commentaire" : commentaire, "punaise" : punaise})

        driver.quit()

        self.reviews = liste_avis


    def print_reviews(self):
        print("=" * 20)
        print(f"Reviews de l'hôtel {self.nom}")
        for i, avis in enumerate(self.reviews, 1):
            print()
            print("============= PUNAISES DE LITS") if "punaise" in avis["commentaire"].lower() else None
            print(f"{i}e avis : \nNote : {avis['note']}\nCommentaire : {avis['commentaire']}")
        print("=" * 20)
        print(f"Il y a {self.nb_comm_punaise_de_lits} commentaires évoquant les punaises de lits pour {self.nom}")


    def to_csv(self):
        csv_columns = ["note","date", "commentaire", "punaise"]
        try:
            with open(f"{self.nom}.csv", 'w',encoding = 'utf8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in self.reviews:
                    writer.writerow(data)
        except IOError:
            print("I/O error")


####### MAIN #######
if __name__ == "__main__":
    for hotel in hotels:
        h = Hotel(endpoint_search+hotel["nom"]+"+"+hotel["commune"], hotel["nom"])
        h.print_reviews()
        h.to_csv()
        break