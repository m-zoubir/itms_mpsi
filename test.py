import requests
import json
import time
import sys

# Configure API URL
BASE_URL = "https://itms-mpsi.onrender.com/api/"  # Change this to your actual API URL

# Configure authentication
# If you're using token auth, you can set it here
HEADERS = {
    "Content-Type": "application/json",
    # "Authorization": "Token YOUR_TOKEN_HERE"  # Uncomment and add your token if needed
}

# Load data from the JSON file or use the embedded JSON
data = {
  "categories": [
    {
      "designation": "Carte mère"
    },
    {
      "designation": "Processeur"
    },
    {
      "designation": "Mémoire"
    },
    {
      "designation": "Stockage"
    }
  ],
  
  "components": [
    {
      "type_composant": "Nouveau",
      "model_reference": "DDR4-16GB-3200",
      "numero_serie": "MEM2023001",
      "designation": "RAM DDR4 16GB 3200MHz",
      "observation": "Barrettes de mémoire neuves",
      "categorie": 3,
      "quantity": 5,
      "disponible": True
    },
    {
      "type_composant": "Nouveau",
      "model_reference": "DDR4-8GB-2666",
      "numero_serie": "MEM2023002",
      "designation": "RAM DDR4 8GB 2666MHz",
      "observation": "Barrettes de mémoire standard",
      "categorie": 3,
      "quantity": 8,
      "disponible": True
    },
    {
      "type_composant": "Nouveau",
      "model_reference": "SSD-500GB-SATA",
      "numero_serie": "SSD2023001",
      "designation": "SSD 500GB SATA III",
      "observation": "Disques SSD pour remplacement",
      "categorie": 4,
      "quantity": 4,
      "disponible": True
    },
    {
      "type_composant": "Nouveau",
      "model_reference": "HDD-1TB-7200",
      "numero_serie": "HDD2023001",
      "designation": "Disque Dur 1TB 7200RPM",
      "observation": "Disques durs standards pour remplacement",
      "categorie": 4,
      "quantity": 6,
      "disponible": True
    },
    {
      "type_composant": "Nouveau",
      "model_reference": "CPU-I5-10GEN",
      "numero_serie": "CPU2023001",
      "designation": "Intel Core i5 10ème génération",
      "observation": "Processeurs de remplacement pour postes de travail",
      "categorie": 2,
      "quantity": 2,
      "disponible": True
    },
    {
      "type_composant": "Nouveau",
      "model_reference": "CPU-I7-10GEN",
      "numero_serie": "CPU2023002",
      "designation": "Intel Core i7 10ème génération",
      "observation": "Processeurs haute performance pour stations de travail",
      "categorie": 2,
      "quantity": 1,
      "disponible": True
    },
    {
      "type_composant": "Nouveau",
      "model_reference": "MB-DELL-790",
      "numero_serie": "MB2023001",
      "designation": "Carte mère Dell OptiPlex 790",
      "observation": "Cartes mères de remplacement pour parc informatique",
      "categorie": 1,
      "quantity": 2,
      "disponible": True
    },
    {
      "type_composant": "Ancien",
      "model_reference": "RAM-HP-8GB",
      "numero_serie": "RAMHP001",
      "designation": "Barrette RAM 8GB HP récuperée",
      "observation": "RAM récupérée d'un PC HP hors service",
      "categorie": 3,
      "numero_serie_eq_source": "HPDT78921",
      "numero_inventaire_eq_source": "INV-2022-001",
      "status": "Free"
    },
    {
      "type_composant": "Ancien",
      "model_reference": "RAM-DELL-4GB",
      "numero_serie": "RAMDELL001",
      "designation": "Barrette RAM 4GB Dell récuperée",
      "observation": "RAM récupérée d'un PC Dell Optiplex hors service",
      "categorie": 3,
      "numero_serie_eq_source": "DELL45672",
      "numero_inventaire_eq_source": "INV-2022-002",
      "status": "Free"
    },
    {
      "type_composant": "Ancien",
      "model_reference": "CPU-I3-4GEN",
      "numero_serie": "CPUI3001",
      "designation": "Processeur Intel i3 4ème génération récupéré",
      "observation": "CPU récupéré d'un PC HP hors service",
      "categorie": 2,
      "numero_serie_eq_source": "HPDT78921",
      "numero_inventaire_eq_source": "INV-2022-001",
      "status": "Free"
    },
    {
      "type_composant": "Ancien",
      "model_reference": "CPU-I5-7GEN",
      "numero_serie": "CPUI5001",
      "designation": "Processeur Intel i5 7ème génération récupéré",
      "observation": "CPU récupéré d'un PC Dell hors service",
      "categorie": 2,
      "numero_serie_eq_source": "DELL45672",
      "numero_inventaire_eq_source": "INV-2022-002",
      "status": "Free"
    },
    {
      "type_composant": "Ancien",
      "model_reference": "HDD-DELL-500GB",
      "numero_serie": "HDDDELL001",
      "designation": "Disque dur 500GB SATA Dell récupéré",
      "observation": "HDD récupéré d'un PC Dell hors service",
      "categorie": 4,
      "numero_serie_eq_source": "DELL45672",
      "numero_inventaire_eq_source": "INV-2022-002",
      "status": "Free"
    },
    {
      "type_composant": "Ancien",
      "model_reference": "MB-HP-8300",
      "numero_serie": "MBHP001",
      "designation": "Carte mère HP EliteDesk 8300 récupérée",
      "observation": "Carte mère récupérée d'un PC HP hors service",
      "categorie": 1,
      "numero_serie_eq_source": "HPDT78921",
      "numero_inventaire_eq_source": "INV-2022-001",
      "status": "Free"
    },
    {
      "type_composant": "Ancien",
      "model_reference": "HDD-HP-1TB",
      "numero_serie": "HDDHP001",
      "designation": "Disque dur 1TB SATA HP récupéré",
      "observation": "HDD récupéré d'un PC HP hors service",
      "categorie": 4,
      "numero_serie_eq_source": "HPDT78921",
      "numero_inventaire_eq_source": "INV-2022-001",
      "status": "Free"
    },
    {
      "type_composant": "Ancien",
      "model_reference": "MB-DELL-3020",
      "numero_serie": "MBDELL001",
      "designation": "Carte mère Dell OptiPlex 3020 récupérée",
      "observation": "Carte mère récupérée d'un PC Dell hors service",
      "categorie": 1,
      "numero_serie_eq_source": "DELL45672",
      "numero_inventaire_eq_source": "INV-2022-002",
      "status": "Free"
    },
    {
      "type_composant": "Nouveau",
      "model_reference": "VGA-GT730",
      "numero_serie": "VGA2023001",
      "designation": "Carte graphique Nvidia GT730 2GB",
      "observation": "Cartes graphiques basiques pour postes standards",
      "categorie": 1,
      "quantity": 3,
      "disponible": True
    },
    {
      "type_composant": "Nouveau",
      "model_reference": "SSD-NVME-256",
      "numero_serie": "SSD2023002",
      "designation": "SSD NVMe 256GB",
      "observation": "SSD haute performance pour postes critiques",
      "categorie": 4,
      "quantity": 2,
      "disponible": True
    },
    {
      "type_composant": "Nouveau",
      "model_reference": "PWR-500W",
      "numero_serie": "PWR2023001",
      "designation": "Alimentation ATX 500W",
      "observation": "Alimentations de rechange",
      "categorie": 1,
      "quantity": 4,
      "disponible": True
    },
    {
      "type_composant": "Ancien",
      "model_reference": "PWR-DELL-300W",
      "numero_serie": "PWRDELL001",
      "designation": "Alimentation Dell 300W récupérée",
      "observation": "Alimentation récupérée d'un PC Dell hors service",
      "categorie": 1,
      "numero_serie_eq_source": "DELL45672",
      "numero_inventaire_eq_source": "INV-2022-002",
      "status": "Free"
    },
    {
      "type_composant": "Ancien",
      "model_reference": "PWR-HP-350W",
      "numero_serie": "PWRHP001",
      "designation": "Alimentation HP 350W récupérée",
      "observation": "Alimentation récupérée d'un PC HP hors service",
      "categorie": 1,
      "numero_serie_eq_source": "HPDT78921",
      "numero_inventaire_eq_source": "INV-2022-001",
      "status": "Free"
    }
  ],
  
  "demandes": [
    {
      "type_materiel": "Ordinateur",
      "marque": "Dell",
      "numero_inventaire": "INV-2023-001",
      "service_affectation": "Département Informatique",
      "nom_deposant": "Ahmed Bensaid",
      "numero_telephone": "0612345678",
      "email": "ahmed.bensaid@example.com",
      "status": "Enseignant",
      "panne_declaree": "L'ordinateur ne s'allume plus du tout",
      "status_demande": "Acceptee"
    },
    {
      "type_materiel": "Imprimante",
      "marque": "HP",
      "numero_inventaire": "INV-2023-002",
      "service_affectation": "Administration",
      "nom_deposant": "Fatima Zahra",
      "numero_telephone": "0623456789",
      "email": "fatima.zahra@example.com",
      "status": "Employe",
      "panne_declaree": "L'imprimante affiche une erreur de cartouche",
      "status_demande": "Acceptee"
    },
    {
      "type_materiel": "Ordinateur",
      "marque": "Lenovo",
      "numero_inventaire": "INV-2023-003",
      "service_affectation": "Bibliothèque",
      "nom_deposant": "Karim Alaoui",
      "numero_telephone": "0634567890",
      "email": "karim.alaoui@example.com",
      "status": "Employe",
      "panne_declaree": "L'écran affiche des lignes horizontales",
      "status_demande": "Acceptee"
    },
    {
      "type_materiel": "Serveur",
      "marque": "HP",
      "numero_inventaire": "INV-2023-004",
      "service_affectation": "Centre de données",
      "nom_deposant": "Mohammed Tazi",
      "numero_telephone": "0645678901",
      "email": "mohammed.tazi@example.com",
      "status": "Enseignant",
      "panne_declaree": "Le serveur redémarre aléatoirement",
      "status_demande": "Acceptee"
    },
    {
      "type_materiel": "Ordinateur",
      "marque": "HP",
      "numero_inventaire": "INV-2023-005",
      "service_affectation": "Département Mathématiques",
      "nom_deposant": "Amina Bennis",
      "numero_telephone": "0656789012",
      "email": "amina.bennis@example.com",
      "status": "Enseignant",
      "panne_declaree": "Surchauffe et extinctions brutales",
      "status_demande": "Acceptee"
    },
    {
      "type_materiel": "Imprimante",
      "marque": "Epson",
      "numero_inventaire": "INV-2023-006",
      "service_affectation": "Département Physique",
      "nom_deposant": "Hassan Ouazzani",
      "numero_telephone": "0667890123",
      "email": "hassan.ouazzani@example.com",
      "status": "Enseignant",
      "panne_declaree": "Bourrage papier constant",
      "status_demande": "Rejetee"
    },
    {
      "type_materiel": "Ordinateur",
      "marque": "Dell",
      "numero_inventaire": "INV-2023-007",
      "service_affectation": "Laboratoire Chimie",
      "nom_deposant": "Nadia Chaoui",
      "numero_telephone": "0678901234",
      "email": "nadia.chaoui@example.com",
      "status": "Employe",
      "panne_declaree": "Système très lent, possiblement infecté",
      "status_demande": "Acceptee"
    },
    {
      "type_materiel": "Autre",
      "marque": "Logitech",
      "numero_inventaire": "INV-2023-008",
      "service_affectation": "Salle de conférence",
      "nom_deposant": "Samir El Mansouri",
      "numero_telephone": "0689012345",
      "email": "samir.elmansouri@example.com",
      "status": "Employe",
      "panne_declaree": "Projecteur qui s'éteint après quelques minutes",
      "status_demande": "Rejetee"
    },
    {
      "type_materiel": "Ordinateur",
      "marque": "Acer",
      "numero_inventaire": "INV-2023-009",
      "service_affectation": "Salle informatique",
      "nom_deposant": "Rachid Benjelloun",
      "numero_telephone": "0690123456",
      "email": "rachid.benjelloun@example.com",
      "status": "Etudiant",
      "panne_declaree": "Le clavier ne répond plus",
      "status_demande": "Nouvelle"
    },
    {
      "type_materiel": "Serveur",
      "marque": "Dell",
      "numero_inventaire": "INV-2023-010",
      "service_affectation": "Département Recherche",
      "nom_deposant": "Leila Bouazza",
      "numero_telephone": "0701234567",
      "email": "leila.bouazza@example.com",
      "status": "Enseignant",
      "panne_declaree": "Problème de disque dur, bruits anormaux",
      "status_demande": "Acceptee"
    },
    {
      "type_materiel": "Ordinateur",
      "marque": "HP",
      "numero_inventaire": "INV-2023-011",
      "service_affectation": "Service scolarité",
      "nom_deposant": "Younes Hamidi",
      "numero_telephone": "0712345678",
      "email": "younes.hamidi@example.com",
      "status": "Employe",
      "panne_declaree": "Problème de connexion Wi-Fi",
      "status_demande": "Nouvelle"
    },
    {
      "type_materiel": "Imprimante",
      "marque": "Brother",
      "numero_inventaire": "INV-2023-012",
      "service_affectation": "Service comptabilité",
      "nom_deposant": "Meryem Idrissi",
      "numero_telephone": "0723456789",
      "email": "meryem.idrissi@example.com",
      "status": "Employe",
      "panne_declaree": "Qualité d'impression très mauvaise",
      "status_demande": "Acceptee"
    },
    {
      "type_materiel": "Ordinateur",
      "marque": "Lenovo",
      "numero_inventaire": "INV-2023-013",
      "service_affectation": "Direction",
      "nom_deposant": "Hamid Ziani",
      "numero_telephone": "0734567890",
      "email": "hamid.ziani@example.com",
      "status": "Employe",
      "panne_declaree": "Problème de batterie, ne tient pas la charge",
      "status_demande": "Acceptee"
    },
    {
      "type_materiel": "Autre",
      "marque": "Samsung",
      "numero_inventaire": "INV-2023-014",
      "service_affectation": "Salle multimédia",
      "nom_deposant": "Laila Benomar",
      "numero_telephone": "0745678901",
      "email": "laila.benomar@example.com",
      "status": "Enseignant",
      "panne_declaree": "Écran tactile qui ne répond plus",
      "status_demande": "Rejetee"
    },
    {
      "type_materiel": "Ordinateur",
      "marque": "Dell",
      "numero_inventaire": "INV-2023-015",
      "service_affectation": "Département Langues",
      "nom_deposant": "Mourad Fathi",
      "numero_telephone": "0756789012",
      "email": "mourad.fathi@example.com",
      "status": "Enseignant",
      "panne_declaree": "Ventilateur bruyant et surchauffe",
      "status_demande": "Nouvelle"
    }
  ],
  
  "interventions": [
    {
      "demande_id": 1,
      "technicien": 1,
      "numero_serie": "DELL-XPS-001",
      "priorite": "Haute",
      "panne_trouvee": "Alimentation défectueuse, remplacement effectué",
      "composants_utilises": [17],
      "status": "Termine"
    },
    {
      "demande_id": 2,
      "technicien": 1,
      "numero_serie": "HP-LJ-002",
      "priorite": "Moyenne",
      "panne_trouvee": "Rouleau d'entraînement papier usé, nettoyage effectué",
      "composants_utilises": [],
      "status": "Termine"
    },
    {
      "demande_id": 3,
      "technicien": 2,
      "numero_serie": "LEN-TH-003",
      "priorite": "Basse",
      "panne_trouvee": "Carte graphique défectueuse, carte mère endommagée",
      "composants_utilises": [],
      "status": "Irreparable"
    },
    {
      "demande_id": 4,
      "technicien": 2,
      "numero_serie": "HP-SRV-004",
      "priorite": "Haute",
      "panne_trouvee": "Problème de RAM, remplacement effectué",
      "composants_utilises": [1],
      "status": "Termine"
    },
    {
      "demande_id": 5,
      "technicien": 1,
      "numero_serie": "HP-DT-005",
      "priorite": "Moyenne",
      "panne_trouvee": "Ventilateur obstrué, nettoyage nécessaire",
      "composants_utilises": [],
      "status": "enCours"
    },
    {
      "demande_id": 7,
      "technicien": 3,
      "numero_serie": "DELL-LT-007",
      "priorite": "Moyenne",
      "panne_trouvee": "Disque dur défectueux, remplacement effectué",
      "composants_utilises": [3],
      "status": "Termine"
    },
    {
      "demande_id": 10,
      "technicien": 3,
      "numero_serie": "DELL-SRV-010",
      "priorite": "Haute",
      "panne_trouvee": "Multiple disques durs endommagés, carte mère défectueuse",
      "composants_utilises": [],
      "status": "Irreparable"
    },
    {
      "demande_id": 12,
      "technicien": 2,
      "numero_serie": "BR-MFC-012",
      "priorite": "Basse",
      "panne_trouvee": "Tête d'impression à remplacer",
      "composants_utilises": [],
      "status": "enCours"
    },
    {
      "demande_id": 13,
      "technicien": 1,
      "numero_serie": "LEN-TP-013",
      "priorite": "Moyenne",
      "panne_trouvee": "Batterie morte, dégâts importants sur la carte mère suite à une fuite",
      "composants_utilises": [],
      "status": "Irreparable"
    }
  ],
  
  "equipements": [
    {
      "model_reference": "LEN-ThinkPad-T480",
      "numero_serie": "LEN-TH-003",
      "designation": "Lenovo ThinkPad T480 - Réformé pour dommages irréparables",
      "observation": "Carte graphique défectueuse, carte mère endommagée. Mis en réforme suite à intervention #3",
      "numero_inventaire": "INV-2023-003"
    },
    {
      "model_reference": "DELL-PowerEdge-R740",
      "numero_serie": "DELL-SRV-010",
      "designation": "Dell PowerEdge R740 - Réformé pour dommages irréparables",
      "observation": "Multiple disques durs endommagés, carte mère défectueuse. Mis en réforme suite à intervention #7",
      "numero_inventaire": "INV-2023-010"
    },
    {
      "model_reference": "LEN-ThinkPad-X1",
      "numero_serie": "LEN-TP-013",
      "designation": "Lenovo ThinkPad X1 - Réformé pour dommages irréparables",
      "observation": "Batterie morte, dégâts importants sur la carte mère suite à une fuite. Mis en réforme suite à intervention #9",
      "numero_inventaire": "INV-2023-013"
    }
  ]
}

# ================== Create Categories ==================
for category in data["categories"]:
    response = requests.post(f"{BASE_URL}categories/", json=category)
    print(f"Category {category['designation']}: {response.status_code}")

# ================== Create Components ==================
for component in data["components"]:
    # Convert category position to ID (assuming creation order)
    component["categorie"] = data["categories"].index(next(
        c for c in data["categories"] if c["designation"] == ["Carte mère", "Processeur", "Mémoire", "Stockage"][component["categorie"]-1]
    )) + 1
    
    response = requests.post(f"{BASE_URL}composants/", json=component)
    print(f"Component {component['designation']}: {response.status_code}")

# ================== Create Demandes ==================
for demande in data["demandes"]:
    response = requests.post(f"{BASE_URL}demandes/", json=demande)
    print(f"Demande {demande['numero_inventaire']}: {response.status_code}")

# ================== Create Interventions ================== 
for intervention in data["interventions"]:
    intervention["technicien"] = 1  # Force technicien ID to 1
    response = requests.post(f"{BASE_URL}interventions/", json=intervention)
    print(f"Intervention for demande {intervention['demande_id']}: {response}")

# ================== Create Equipements ==================
for equipement in data["equipements"]:
    response = requests.post(f"{BASE_URL}equipements/", json=equipement)
    print(f"Equipement {equipement['numero_inventaire']}: {response.status_code}")

print("All data seeded successfully!")