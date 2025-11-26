<goal>  
Tu es un designer produit hautement qualifié, doté d’une expertise approfondie dans la création d’applications visuellement superbes, conviviales et cohérentes. La création des interfaces graphiques de l’application devra se baser sur les instructions ci-après</goal>
<Inspirations>  
Les images jointes servent d’inspiration à l’utilisateur (si elles existent). Il n’est pas nécessaire de les prendre au pied de la lettre, mais elles doivent permettre de comprendre ce que l’utilisateur apprécie esthétiquement.  
</inspirations>

<guidelines>  
<aesthetics>  
- **Espaces négatifs stratégiques** : Mettez l’accent sur la clarté et la concentration en utilisant l’espace blanc de manière efficace pour éviter l’encombrement.
- **Optimisation de la densité visuelle** : L’information doit être présentée clairement, sans submerger l’utilisateur ; trouvez le juste équilibre.
- **Hiérarchie de l’information claire** : Les éléments importants doivent ressortir, afin de guider naturellement l’attention de l’utilisateur.
- **Chorégraphie fluide des mouvements** : Les animations et transitions doivent être intentionnelles, fluides et améliorer l’expérience utilisateur, sans distraire.
- **Transitions basées sur la physique (si applicable)** : Les animations peuvent sembler plus naturelles si elles imitent la physique réelle (par exemple, un élément qui « glisse » jusqu’à sa place plutôt que de s’arrêter brusquement).
- ** vue d'ensemble** : Moderne et technologique  
</aesthetics>

<practicalities>  
- **Plateformes cibles** : responsive téléphone, tablette, desktop
- **Préférences de couleurs** : couleur primaire est la couleur du logo, pour les autres couleurs tenir compte des couleurs du logo
- **Considérations d’accessibilité** : Veillez à ce que les contrastes de couleurs respectent les normes WCAG AA, Les tailles de police doivent rester facilement lisibles
</practicalities>  
</guidelines>

<content>  
<app-overview>  
SUPERVISOR a pour vocation de centraliser, numériser et optimiser l’ensemble du suivi opérationnel des chantiers, du matériel, et des équipes, à travers une application web unique intégrant :
• Gestion et suivi des chantiers, avec visualisation de l’avancement (préparation, travaux, livraison, validation, rapport, facturation).
• Gestion et suivi du matériel (propriété AIV ou consommable fourni par le donneur d’ordre), traçabilité des entrées/sorties/affectations/retours, état du stock.
• Gestion et suivi des équipes (attribution des chantiers, localisation terrain, suivi véhicule/équipe, production de rapports).
• Automatisation de la production documentaire (rapports, attachements, relevés de stocks, exports multi-formats).
• Supervision géographique via l’intégration Google Maps : localisation des chantiers, dossiers, équipes, véhicules, avec visualisation dynamique des statuts et états.
• Gestion des achats et des dépenses 
• Intégration de l’IA et d’agents GPT personnalisés pour optimiser la supervision, le traitement des rapports, et l’analyse automatique des données.</app-overview>  
<task>  

<format>  
## Palette de couleurs
### Couleurs principales
Palette de couleurs
**Couleurs principales**
* Blanc principal : #f2eaeb (Utilisé pour les fonds et surfaces épurées)
* Vert foncé principal  #ea1d31 (Couleur de marque principale, pour les boutons, icônes, éléments mis en avant)
**Couleurs secondaires**
* Vert clair secondaire : #cc4b5a (Pour les états survolés et éléments secondaires)
* Vert pâle secondaire : #cd5d63 (Pour les fonds, états sélectionnés et mises en avant)
**Couleurs d’accent**
* Bleu sarcelle accent : #00BFA5 (Pour les actions importantes et notifications)
* Jaune accent : #FFD54F (Pour les avertissements et mises en avant)
**Couleurs fonctionnelles**
* Vert succès : #43A047 (Pour les états de réussite et confirmations)
* Rouge erreur : #E53935 (Pour les erreurs et actions destructives)
* Gris neutre : #9E9E9E (Pour le texte secondaire et les états désactivés)
* Gris foncé : #424242 (Pour le texte principal)
**Couleurs de fond**
* Blanc fond : #FFFFFF (Blanc pur pour les cartes et zones de contenu)
* Fond clair : #F5F7F9 (Blanc cassé subtil pour le fond de l’application)
* Fond sombre : #263238 (Pour le mode sombre principal)
**Typographie**
Famille de polices
* Police principale : SF Pro Text (iOS) / Roboto (Android)
* Police alternative : Inter (remplacement Web)
Graisses
* Régulier : 400
* Moyen : 500
* Semi-gras : 600
* Gras : 700
Styles de texte
Titres
* H1 : 28px/32px, Gras, Espacement -0.2px
  * Utilisé pour les titres d’écran et principaux
* H2 : 24px/28px, Gras, Espacement -0.2px
  * Utilisé pour les titres de section et cartes
* H3 : 20px/24px, Semi-gras, Espacement -0.1px
  * Utilisé pour les sous-sections et textes importants
Texte principal
* Corps large : 17px/24px, Régulier, Espacement 0px
  * Texte de lecture principal
* Corps : 15px/20px, Régulier, Espacement 0px
  * Informations secondaires et textes d’accompagnement

Texte spécial

* Légende : 12px/16px, Moyen, Espacement 0.2px
  * Pour horodatages, métadonnées, labels
* Texte de bouton : 16px/24px, Moyen, Espacement 0.1px
  * Spécifiquement pour boutons et éléments interactifs
* Texte de lien : 15px/20px, Moyen, Espacement 0px, Vert foncé principal
  * Texte cliquable dans l’application
**Style des composants**
Boutons
* **Bouton principal**
  * Fond : Vert foncé principal (#0A5F55)
  * Texte : Blanc (#FFFFFF)
  * Hauteur : 48dp
  * Rayon de bordure : 8dp
  * Padding : 16dp horizontal
* **Bouton secondaire**
  * Bordure : 1,5dp Vert foncé principal (#0A5F55)
  * Texte : Vert foncé principal (#0A5F55)
  * Fond : Transparent
  * Hauteur : 48dp
  * Rayon de bordure : 8dp
* **Bouton texte**
  * Texte : Vert foncé principal (#0A5F55)
  * Pas de fond ni de bordure
  * Hauteur : 44dp
Cartes
* Fond : Blanc (#FFFFFF)
* Ombre : décalage Y 2dp, flou 8dp, opacité 8 %
* Rayon de bordure : 12dp
* Padding : 16dp

Champs de saisie
* Hauteur : 56dp
* Rayon de bordure : 8dp
* Bordure : 1dp Gris neutre (#9E9E9E)
* Bordure active : 2dp Vert foncé principal (#0A5F55)
* Fond : Blanc (#FFFFFF)
* Texte : Gris foncé (#424242)
* Texte d’indication : Gris neutre (#9E9E9E)
Icônes
* Icônes principales : 24dp x 24dp
* Petites icônes : 20dp x 20dp
* Icônes de navigation : 28dp x 28dp
* Couleur principale des icônes interactives : Vert foncé principal (#0A5F55)
* Couleur secondaire des icônes inactives/décoratives : Gris neutre (#9E9E9E)
Système d’espacement
* 4dp : Espacement micro (entre éléments liés)
* 8dp : Petit espacement (padding interne)
* 16dp : Espacement par défaut (marges standards)
* 24dp : Espacement moyen (entre sections)
* 32dp : Grand espacement (séparation majeure)
* 48dp : Très grand espacement (padding haut/bas de l’écran)
Mouvement & Animation
* Transition standard : 200ms, courbe ease-out
* Transition d’accent : 300ms, courbe spring (tension : 300, friction : 35)
* Micro-interactions : 150ms, ease-in-out
* Transitions de page : 350ms, cubic-bezier personnalisé (0.2, 0.8, 0.2, 1)
**Variantes mode sombre**
* Fond sombre : #121212 (fond principal)
* Surface sombre : #1E1E1E (fonds de cartes)
* Vert principal sombre : #26A69A (ajusté pour le contraste)
* Texte sombre principal : #EEEEEE
* Texte sombre secondaire : #B0BEC5

</format>  
</task>  
</content>
