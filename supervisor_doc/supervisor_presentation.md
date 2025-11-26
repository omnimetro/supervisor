# PRESENTATION DE L'APPLICATION SUPERVISOR
I. Compréhension du besoin

AI Venture (AIV) intervient en tant que sous-traitant pour le compte
d’opérateur, sur des projets de déploiement, raccordement et maintenance de
réseaux de fibre optique. AIV peut avoir recours à d’autres entreprises sous-
traitantes pour réaliser certaines parties des travaux.
L’entreprise gère :

-Des chantiers de déploiement (backbone, réseaux de transport,
distribution)
-Des raccordements B2B (entreprises clientes),
-De la maintenance sur les réseaux fibrés existants.
```
Dans la gestion de ses activités, 4 fonction essentielles sont mises en œuvre :

- La gestion de l’exécution des travaux
- La gestion des stocks de matériels et consommables
- La gestion des dépenses de liées à la réalisation des différents travaux
- La gestion de la facturation

I.1. La gestion de l’exécution des travaux

Il y a principalement 2 types travaux :

- Les chantiers de déploiement : réalisation de réseaux de transport,
    réalisation de backbone et la réalisation de réseaux de distribution.
- Les raccordements b2b et maintenances b2b : la réalisation de travaux de
    connexion des clients finaux à internet et leurs maintenances.

I.1.1. La gestion de l’exécution des travaux de déploiement

Les chantiers de déploiement concernent la réalisation de réseaux de transport,
de backbone ou de réseaux de distributions.

A l’ouverture d’un chantier, L’opérateur remet à AIV la documentation
concernant le chantier à savoir le plan synoptique (architecture réseau
des équipements télécoms à installer sur le chantier), le plan Map (le
chemin des câbles et les positions des équipements télécom sur un plan
de la zone du chantier), le BOM (quantitatif des consommables
nécessaires à la réalisation du projet)
Les différentes informations du chantier sont :
```
- Code du chantier
- Site du chantier
- Le code de l’opérateur
- Type de chantier ( backbone, transport ou déploiement)
- Date de début
- Superviseur opérateur
- Superviseur AIV
- Travaux ok
- Environnement ok
- Vt ok
- Pv ok
- Date de livraison
    Un chantier appartient à un opérateur
1) Exécution des travaux

Les travaux sont exécutés sur plusieurs étapes :

- Travaux GC
- Travaux de réseau
- Travaux FO

Chaque opérateur possède sa propre nomenclature de travaux. La
nomenclature d’un opérateur contient la liste des travaux avec le prix unitaire
de chaque travail, le document est appelé BOQ. C’est sur la base de son BOQ
qu’un opérateur contrôle et valide les travaux.

Les fichiers joints travaux_orange.xls et travaux_moov.xls sont les BOQ des
opérateurs Orange et Moov.Les information du BOQ pour chaque travail :

- La catégorie du travail (travaux GC, travaux de réseau, travaux FO)
- Le libellé du travail
- L’unité de mesure

A partir du BOQ de l’opérateur, AIV définit les tâches qui doivent être
accomplies par AIV et/ou ses sous-traitants pour la réalisation de chaque
travail.

Les information de la tâche sont :

- Le code et libellé du travail
- Code et Libellé de la tâche
- Unité de mesure
- KPI (qte/jour)

A partir du BOQ de l’opérateur, un planning des travaux avec les quantitatif est
élaboré pour le chantier à exécuter. Ce planning ne prend en compte que les
travaux concernés par le chantier.

Les informations d’un planning prévisionnel d’un travail sont :

- Le code du chantier
- La catégorie du travail
- Le nom du travail
- La quantité prévisionnelle
- Le délai de réalisation en nombre de jours

Après le planning prévisionnel des travaux, un planning prévisionnel des taches
est élaboré pour chaque travail à exécuter sur le chantier. Un planning
prévisionnel des tâches pour un travail à exécuter se présente de la manière
suivante :

- Code du chantier
- Catégorie du travail
- Code et libellé du travail
- Code et libellé de la tâche
- Quantité prévisionnelle
- Délai de réalisation en nombre de jour
- Date début
- Date de fin

Les tâches d’un travail sont effectuées soit par des techniciens de AIV soit par
les techniciens d’une entreprise sous-traitante sélectionnée par AIV. Sur chaque
chantier est affecté un superviseur de l’opérateur, un superviseur de AIV et un
superviseur du sous-traitant dans le cas où AIV confie une partie des travaux à
un sous-traitant

Chaque jour un reporting des tâches de chaque travail en cours est effectué par
le superviseur AIV

. Pour chaque tâche, le reporting contient les informations suivantes :
    - La date du jour
    - Code et libellé du travail (tiré du planning du travail)
    - Code et libellé de la tâche exécutée
    - Le quantitatif du jour
    - Code de La structure qui a effectué le travail (AIV ou un sous-traitant)
    - Le code du référent (le technicien superviseur AIV)
    - Les observations
    - Les photos notecam

Pendant l’exécution des travaux les positions gps des différents points
nécessaires à la cartographie du chantier sont enregistrés dans une fiche
cartographie ce sont : les poteaux implantés (métallique ou béton), les
équipements, les chambre, travaux gc. Les gps sont extraits des photos
notecam prises lors des reporting.

Une fiche cartographie se présente de la manière suivante :

- Date
- Localité
- Code chantier
- Type d’infrastructure ou équipement (poteau béton ou métallique,
    pec, pco, pep, jdv...)
- Latitude
- Longitude

L’exécution de tous les travaux de toutes les étapes marque la fin de la phase
des travaux.

```
2) Phase de livraison
```
La phase de livraison se déroule selon les étapes suivantes :

Etape 1 : environnement et contrôle interne

Durant ceƩe étape l’on procède au neƩoyage de l’environnement et au contrôle
par un superviseur de AIV afin de déceler d’éventuelles erreurs et les corriger.
Les corrections sont enregistrées de la manière suivantes

- Le code du chantier
- Date
- Code et libellé du travail
- Code et libellé de la tâche
- Statut (ok, non ok)
- Observations
- Photos notecam

Etape 2 : rédaction de rapport de fin de chantier (RFC)

Un rapport de fin de chantier (format powerpoint) est rédigé selon le modèle
fourni par l’opérateur

Etape 3 : visite technique de l’opérateur

Le superviseur de l’opérateur procède à une visite technique au fin de déceler
les erreurs et les faire corriger

En cas de correction d’erreurs, un rapport de correction est rédigé à la fin de la
correction.

A la fin d’un chantier, à partir du BOQ, un récap des travaux effectués avec les
quantités est saisi dans un fichier Excel dont le modèle est fourni par
l’opérateur.

I.1.2 les raccordements et maintenances b2b

Les équipes b2b sont reparties sur des zone géographiques de manière fixe.
Chaque équipe b2b traite les dossiers de raccordement et de maintenance de
sa zone. Chaque équipe b2b est dirigée par un chef d’équipe.

Chaque jour l’opérateur envoie par message (mail, WhatsApp) la liste des
dossiers de raccordement b2b et la liste des dossiers de maintenance b2b et de
maintenance de déploiement.

Il s’agit de personnes physiques ou morales qui ont souscrit à un abonnement à
internet par fibre optique auprès de l’opérateur et dont il faut faire le
raccordement (nouveau abonné) ou la maintenance (ancien abonné)

Un dossier client contient les informations suivantes :

- Code du dossier
- Date de réception
- Nom et prénoms du client
- Zone géographique
- Contact 1
- Contact 2
- Coordonnés GPS (longitude et latitude du client)
- Type d’intervention (raccordement ou maintenance b2b, maintenance de
    déploiement)
- Statut final (corbeille, etudeOK, maintenanceOK, problème client, client
    hors zone ...)
    Le raccordement est fait en 2 étapes :

Etude : localisation effective du client, localisation du pco proche du
client, évaluation du nombre de poteaux à implanter. Tous ces élément
permeƩent de déterminer si le client peut être installé ou pas.
A l’issue de l’étude, un rapport d’étude est généré. Le rapport d’étude
contient les informations suivantes :
o Code du dossier
o Date d’étude
o Numéro box client
o Cluster
o SRO/PCO
o Latitude et longitude du PCO
o Distribution
o Raccordement fibre
o Plots disponibles
o Distance PCO
o Nombre de poteaux à implanter
o Photo note cam domicile
o Photo note cam du PCO
o Observations
A l’issue de l’étude, le statut du dossier est modifié (étude ok, client hors
zone, pco saturé...)
Raccordement : si le client peut être installé, l’équipe b2b procède à son
raccordement. Après l’installation un rapport d’installation est édité et le
statut du dossier est modifié (raccordement ok)
Le rapport d’installation contient les informations suivantes :
```
- Date
- Code du dossier
- Activation ok (oui ou non)
- Observations
- Matériels utilisés :
    - CÂBLE :
    - COLLIER :
    - PITON :
    - PTO :
    - ATTACHE :
    - BÂTON À COLLE :
    - PINCE :
    - POTEAU IMPLANTE

Pour une maintenance, l’équipe fait directement l’intervention. Après la
maintenance le dossier du client est mis à jour avec la cause du problème et les
actions menées.

A la fin de chaque période (du 20 du mois en cours au 21 du mois suivant), un
récap des interventions effectuées et de la quantité de matériel utilisés est fait
dans un fichier Excel dont le modèle est fourni par l’opérateur.

I.3 La gestion des stocks de matériels et consommables

Tous les équipements et les consommables sont gérés par le service de gestion
de stock de AI VENTURE. Les différents mouvements gestion de stock sont :

Le service de gestion gère 2 types de stock :

```
a) Ressources Matériels appartenant à AI Venture
```
Pour réaliser ses chantiers, AI Venture utilise un ensemble de matériels et
d’équipements, dont :

- Matériels lourds : Véhicules, groupes électrogènes, marteaux-
    piqueurs, motopompes.
- Outils de précision : Soudeuses, réflectomètres, power meters,
    lasers.
- Outils génériques : Perceuses, meules, postes à souder, caisses à
    outils.
- Matériels de sécurité (EPI) : Casques, chasubles, gants.
- Divers consommables : aƩaches, bâtonnet de colle
b) Ressources matériels appartenant à l’opérateur


Pour l’exécution d’un chantier, l’opérateur met à la disposition de AIV un
ensemble de matériels et de consommables :

- Equipement réseau (PCO,JDV,PEC...)
- Consommables (câbles fibres optiques, poteaux métalliques...)

Pour chaque mouvement une fiche de mouvement est remplie :

- Date
- Type entité (technicien, chantier, opérateur, équipe b2b, hors
    stock)
- Rôle entité (origine, destination)
- Code et libellé entité
- Code et libellé matériel
- Type de mouvement (entrée, sortie)
- Type d’opération (inventaire, achat, affectation, indisponibilité,
    intégration, retour matériel, récupération ...)
- Quantité
- RemeƩant (code du technicien qui a remis le matériel)
- Réceptionnaire (code du technicien à qui le matériel a été remis)

Les types d’opérations :

Inventaire : c’est le décompte physique à une période donnée des équipements
et matériels existants dans les entrepôts de AIV

Acquisition : c’est l’ajout d’un matériel ou d’un équipement au stock de AIV
pour la première fois.

Affectation : c’est lorsqu’un matériel est mis à la disposition d’un chantier,
d’une équipe b2b, d’un technicien.

Récupération : c’est lorsqu’un matériel retourne en stock après avoir été utilisé.

Enlèvements : c’est lorsque l’opérateur (opérateur) met du matériel à la
disposition de AIV pour être utilisé sur un chantier ou par une équipe b2b
(raccordement et maintenance).


Retour matériel : c’est lorsque le reste de matériel affecté à un chantier est
retourné à l’opérateur à la fin du chantier

Indisponibilité : c’est lorsqu’un équipement est inutilisable pour une certaine
période pour cause de panne ou autres

Intégration : c’est lorsqu’un matériel qui était inutilisable devient utilisable

Retrait de stock : c’est lorsqu’un matériel sort définitivement du stock de AIV
soit parce qu’il a été vendu, soit parce qu’il est définitivement abimé.

Pour chaque matériel les stocks suivants sont calculés :

QMP (Quantité Matériel Possédé) = Total acquisition – Total retrait de stock

QAffectés (Quantité matériel affecté) = Total affectation – Total récupération

Dispos (Quantité matériel disponible ) = total entrées – total sorties

1.4 la gestion des dépenses liées à l’exécution des chantiers

Les dépenses effectuées dans le cadre de la réalisation des chantiers de
déploiement, des raccordements et des maintenances sont consignées dans
des fiches de dépenses. Une fiche de dépenses peut être liée ou non à un
chantier ou à une équipe b2b. la fiche de dépense contient :

- Type entité (chantier, équipe b2b, technicien)
- Code entité
- La date
- Type dépense (achat , location, prestation, main d’œuvre,
    communication, carburant, per diem)
- La désignation
- Le prix unitaire
- La quantité
- Le montant



Gestion des utilisateurs & sécurité

Authentification sécurisée (login, logout, récupération de mot de passe,
gestion des sessions).

Gestion des rôles et permissions :

Super Administrateur, administrateur, coordonnateur, superviseur, gestionnaire
de stock,

Droits d’accès configurables par module et par action.

Traçabilité des actions :

Journalisation de toutes les actions sensibles (mouvements de stock, validation
de rapport, export, etc.).

Tableaux de bord, rapports & exports

1. Dashboard personnalisable :
    o Vue synthétique (cartes, indicateurs, graphiques, listes d’alertes).
    o Widgets par profil utilisateur (suivi chantiers, stocks, équipe,
       matériel, etc.).
2. Rapports automatisés :
    o Rapports combinant texte, photos, tableaux, graphiques (évolution
       des stocks, avancement des travaux, incidents, etc.).
    o Génération automatique des aƩachements (facturation) selon les
       modèles fournis.
3. Exports multi-formats :
    o Excel, CSV, PDF, Word, images, etc.
    o Export paramétrable par utilisateur.


Intelligence artificielle & automatisation

1. Intégration d’agents GPT & IA :
    o Assistance à la rédaction de rapports et synthèses.
    o Analyse automatique de la qualité des rapports et des
       avancements.
    o Suggestions automatiques (alertes, anomalies, préconisations).
2. Automatisation de tâches :
    o Détection automatique d’incohérences ou de retard dans
       l’avancement.
    o Pré-remplissage de rapports à partir des données structurées et
       non structurées (OCR, photo, voix).

Cartographie

1. Chantiers de déploiement :
    -Transformation du MAP au format PDF en plan cartographique avec
       repère GPS.
    -Insertion du map cartographié dans google maps.
    -Positionnement des équipements : les poteaux implantés (métallique
       ou béton), les équipements, les chambre, travaux gc.
2. Raccordement et maintenance B2B
    -Positionnement du domicile du client sur google maps.
    -Positionnement du PCO raƩaché au client sur google maps.
3. Tracking des véhicules
Pour le traçage des véhicules 2 méthodes seront utilisées :

Pour un véhicule équipé de traceur GPS, le traçage sera effectué avec l’API de
whatsgps et les positions du véhicule seront affichés sur google maps.

Pour un véhicule non équipé de traceur GPS, une application mobile de traçage
sera installée sur le téléphone mobile du chauffeur. CeƩe application enverra
les positions, et elles seront affichées sur google maps.

4. importation en live de fichiers KMZ et affichage de leur contenu sur google maps



Expérience utilisateur et accessibilité (Responsive Design)

1. Responsive design intégral :
    o Interface fluide et réactive, adaptée à tout type d’écran
       (smartphone, tableƩe, laptop, desktop).
    o Composants ajustés automatiquement, menus latéraux ou
       hamburgers selon l’espace disponible.
    o Saisie simplifiée, navigation rapide, boutons d’action accessibles au
       doigt pour un usage mobile sur le terrain.
2. Accessibilité & ergonomie :
    o Contraste élevé, taille de police réglable, raccourcis clavier,
       compatibilité lecteurs d’écran.
    o Temps de chargement optimisé, stockage temporaire local pour
       usage offline/déconnexion terrain.
3. Mode sombre et mode clair :
    o Pour le confort en toute situation (extérieur, nuit).

Paramétrage, notifications & logs

1. Paramétrage avancé :
    o Définition des seuils de stocks, modèles de rapports, listes des
       donneurs d’ordre, etc.
2. Notifications multi-canal :
    o Push sur l’application, emails, WhatsApp, alertes en cas d’incident
       ou d’action requise.
3. Logs & historique :
    o Historique de toutes les modifications, suppression, validation par
       utilisateur.
    o Exports de logs pour audit.
-Interopérabilité : intégration d’APIs externes (Google Maps, WhatsGPS,
WhatsApp, services d’exports...).
-Sécurité & traçabilité : gestion des accès par rôles, journalisation des
opérations sensibles (stock, rapports, affectations).
-Amélioration de la supervision (cartographie dynamique, IA, tableaux de
bord décisionnels).
-Facilité de prise en main pour tous les profils d’utilisateurs
(administrateur, chef de projet, équipe terrain, gestionnaire de stock...).
```
Contraintes et environnement technique

```
-Front-end : quasar js. UI réactive, responsive, ergonomique, adaptée au
terrain (usage sur tableƩe/smartphone possible).mobile first
-Back-end : Django 4.2.16 + Python 3.
-Base de données : MySQL
-Outils de développement : os windows 11, vs code, environnement
virtuel python 3.12, wamp server pour mysql, serveur web intégré pour
les tests.
```
