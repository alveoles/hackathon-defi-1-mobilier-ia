---
defi: 01
titre: SKETCH2CNC
accroche: if (idee) { fabriquer(); }
sous_titre: Une idée ne vaut rien tant qu'elle n'est pas fabriquée.
version: v2
---

## Introduction

Dans le design de mobilier, passer du **croquis** à la **production** (modèle 3D, plans de coupe, rendus marketing) prend des jours, parfois des semaines, d'allers-retours entre le designer, la CAO et l'atelier.

Ta mission, avec ton équipe : construire un **assistant de design** (Proof of Concept). Il ne remplace pas le designer. Il transforme un croquis en propositions photoréalistes, puis en fichiers prêts pour la CAO et la découpe.

L'outil est **« Human-in-the-Loop »** : l'IA propose, le designer décide. Chaque étape clé passe par une validation humaine.

> ℹ️ **Périmètre de la journée :** une **assise en bois** (chaise, tabouret ou fauteuil), destinée à être **découpée à la CNC**.

Le workflow repose sur trois piliers :

- **Le dessin** : passer d'un croquis brut à un croquis exploitable
- **Le rendu** : donner matière, lumière et vues standardisées à l'objet
- **La fabrication** : produire un fichier 3D et des vecteurs de découpe

> ℹ️ Un designer met des jours à passer du croquis au fichier de découpe. Tu as une journée pour prouver que ce délai peut tomber à quelques minutes.

## Considérations techniques

Tu es libre sur les technologies, avec une contrainte : **tout tourne en local, sur ton ordinateur, avec des outils gratuits et open source.** Aucune API payante, aucun service en ligne obligatoire. Il te faudra au minimum :

- une **orchestration IA** (ComfyUI, scripts Python…)
- un **modèle d'image avec contrôle de la forme** : la géométrie du croquis ne doit pas changer d'une étape à l'autre
- une **interface** qui produit le **Dashboard du designer**

> ℹ️ L'open source est ton meilleur allié : des centaines de modèles et de workflows existent déjà. Mais chaque heure passée à installer est une heure en moins pour construire. Choisis vite, et tiens-toi à ton choix.

> ℹ️ Un rendu magnifique dont la forme a dérivé ne sert à rien à un fabricant. La fidélité au croquis passe avant l'esthétique.

> ℹ️ Branches, pull requests, commits lisibles. Ton historique git fait partie du rendu.

## Starter Pack

Dans `starter-pack/`, le process réel d'Anthony pour sa chaise **Atto** :

- `01_Inputs_Croquis/` : le croquis de départ, 3 vues sur une même feuille
- `02_Inputs_References/` : une photo de mobilier existant
- `03_Outputs_Cibles/` : ce qu'Anthony produit aujourd'hui (rendus, mises en situation, modèle Rhino) et `HACKATHON-Process.pdf`, son process en 7 étapes

> ℹ️ Le croquis est un vrai croquis de designer, pas un dessin technique : plusieurs vues, traits de construction, perspective à main levée. Ton outil doit s'en accommoder.

## Fonctionnalités

Les fonctionnalités sont formulées en **user stories** et regroupées par **palier**. À l'intérieur d'un palier, **elles ne sont pas triées** : à ton équipe de les prioriser. Elles sont validées par ton Product Owner pour le seul sprint de la journée.

> ℹ️ Un palier stable et démontrable vaut plus que trois paliers commencés. Ne passe au suivant qu'une fois le précédent solide.

> ℹ️ Toutes les user stories sont-elles claires ? Les comprenez-vous tous de la même façon ?

### Palier 1 : le pipeline 2D

*Étape 1 : du croquis au croquis propre*

- En tant que designer, je veux uploader un croquis, afin de démarrer le workflow
- En tant que designer, je veux que l'IA corrige les perspectives et me propose plusieurs variantes propres, afin de partir d'une base nette
- En tant que designer, je veux orienter les variantes avec un prompt, afin de garder la main sur l'intention
- En tant que designer, je veux sélectionner la variante retenue, afin que la décision reste humaine

*Étape 2 : du croquis au rendu*

- En tant que designer, je veux appliquer une matière de la bibliothèque, afin de visualiser mon assise en bois réel
- En tant que designer, je veux que la forme reste identique à celle de la variante validée, afin que le rendu reste fidèle

*Étape 3 : vues marketing et techniques*

- En tant que designer, je veux générer en une fois les vues de face, de côté, de dessus et en perspective sur fond blanc, afin de constituer une fiche produit
- En tant que designer, je veux une vue « lifestyle » en situation, afin de présenter le produit au client

### Palier 2 : le passage à la 3D

- En tant que designer, je veux obtenir un modèle 3D téléchargeable de mon assise, afin de poursuivre en CAO
- En tant que fabricant, je veux que le modèle 3D respecte les proportions du croquis, afin de fabriquer le bon objet
- En tant que fabricant, je veux que les cotes du croquis soient extraites en JSON pour alimenter un modèle paramétrique, afin d'obtenir une géométrie propre pour la production

> ℹ️ Mesh ou paramétrique ? L'un est plus rapide à obtenir, l'autre bien plus utile en atelier. Fais un choix d'équipe, et sache le défendre.

### Palier 3 : prêt pour la CNC

- En tant que fabricant, je veux des vecteurs de découpe 2D (SVG, DXF), afin de lancer la découpe
- En tant que fabricant, je veux un plan technique simplifié, afin de vérifier les pièces avant la découpe

### Bonus : aller plus loin

- En tant que designer, je veux voir 5 à 10 produits similaires déjà existants, afin de vérifier l'originalité de mon design
- En tant que designer, je veux un moodboard (matériaux, couleurs) tiré de ce benchmark, afin de nourrir le rendu

> ℹ️ Pas besoin d'Internet pour comparer des images : `02_Inputs_References/` et un modèle d'embeddings (CLIP, SigLIP) suffisent pour commencer.

### …

Anthony, le designer, t'a présenté son process (`03_Outputs_Cibles/HACKATHON-Process.pdf`). Il a évoqué UNFNSHED, du mobilier assemblable sans outils, les épaisseurs de panneaux et les contraintes de sa machine. Tout n'est pas écrit dans ce sujet.

> ℹ️ Ton client est dans la salle, et il ouvrira tes fichiers STEP dans son Rhino. Va lui poser tes questions, et sois prêt à formuler de nouvelles user stories.

## Livrable : le Dashboard du designer

À **17h00**, démonstration live via une **page de synthèse générée automatiquement**, qui contient :

- le **croquis original** (« Avant »)
- les **rendus finaux** choisis, sur fond blanc et en situation (« Après »)
- un **visualiseur 3D interactif** (à partir du palier 2)
- un bouton **« Télécharger le package de production »** (images, modèle 3D, vecteurs)
- *(bonus)* la **galerie de benchmark**

Côté repo : un `README` avec les instructions de lancement, des PR fusionnées et un tag **`v1.0-rendu`** avant la démo.
