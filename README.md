# 📌 Fichotron - AI

Fichotron - AI est une application web destinée à automatiser la génération de fiches clients pour SFIL. Ce projet permet de fusionner des données publiques issues de sources telles que data.gouv ou Wikipédia avec des données internes pour produire une fiche client standardisée, précise, complète et modifiable. L'interface utilisateur adopte un design minimaliste, moderne et responsive, offrant une expérience fluide et intuitive.

## Table des matières

- [📌 Fichotron - AI](#-fichotron---ai)
  - [Table des matières](#table-des-matières)
  - [Architecture](#Architecture)
  - [Fonctionnalités](#fonctionnalités)
  - [🖥️ Déploiement](#️-déploiement)
  - [🛠️ Technologies Utilisées](#️-technologies-utilisées)
  - [🎯 Objectifs et Critères de Succès](#-objectifs-et-critères-de-succès)
  - [Contributions](#contributions)
  - [Licence](#licence)
  - [🚀 Réalisé par la LLaMazing Team](#-réalisé-par-la-llamazing-team)

## Architecture

![Architecture](graph.png)

## Fonctionnalités

- **Génération de fiches clients :** 
  - Fusion de données publiques et internes pour générer une fiche client en format Word.
  - Interface moderne et intuitive pour saisir le nom de la ville ou du département.
  
- **Recherche intelligente :**
  - Suggestions de résultats organisées en trois catégories : Régions, Départements et Communes.
  - Filtrage basé sur les caractères de début du mot avec normalisation (gestion des accents et des tirets).

- **Bouton d'importation :**
  - Permet aux utilisateurs d'importer des fichiers de données via un bouton au même style que le bouton "Générer".

- **UI/UX responsive :**
  - Design minimaliste et moderne, adapté à tous types d'écrans (smartphones, tablettes, ordinateurs).
  - Effets d'animation et de transition fluides (hover, focus, scroll).

- **Autres éléments :**
  - Bouton "Retour en haut" pour améliorer la navigation sur la page.

### Scrapping amélioré proto
Un prototype de code de scrapping amélioré se trouve dans le folder Scrapping_impr.
Le scrapping recherche les urls pertinents en fonction d'une liste de thèmes prédéfinis tels que le financement ou de l'écologie.

## 🖥️ Déploiement

Pour déployer le site sur AWS S3 et CloudFront :
  1.	Hébergement S3 :
    •	Mettez à jour votre bucket S3 avec les fichiers du projet (HTML, CSS, JS, images, etc.).
    •	Utilisez l’AWS CLI pour synchroniser le contenu, par exemple :
  ```bash
  aws s3 sync ./ s3://votre-bucket --delete
  ```
  2.	CloudFront :
    •	Configurez une distribution CloudFront pointant vers votre bucket S3.
    •	Effectuez une invalidation du cache pour rafraîchir les contenus après chaque déploiement :
  ```bash
  aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
  ```
  3.	Automatisation (optionnel) :
    •	Utilisez GitHub Actions pour automatiser le déploiement à chaque push sur la branche principale.


## 🛠️ Technologies Utilisées
- AWS CloudFront (Hébergement Frontend)
- AWS API Gateway (Récupération des collectivités)
- AWS Lambda (Traitement automatisé des données)
- DynamoDB (Stockage des liens)
- AWS S3 (Stockage des résultats intermédiaires)
- AWS Bedrock (Génération de contenu à l'aide d'un RAG)

## 🎯 Objectifs et Critères de Succès
- ✅ Implémentation d’un modèle RAG sur AWS pour la génération des fiches
- ✅ Exactitude et complétude des informations collectées
- ✅ Comparaison avec les fiches créées manuellement
- ✅ Adaptabilité aux spécificités des différentes collectivités
- ✅ Optimisation continue grâce aux retours d'expérience

## Contributions

Les contributions sont les bienvenues !
Si vous souhaitez contribuer à ce projet, veuillez soumettre une pull request avec vos améliorations ou corrections. Assurez-vous de suivre les bonnes pratiques de codage et de respecter le style existant.

## Licence

Ce projet est sous licence MIT.

## 🚀 Réalisé par la LLaMazing Team

Ce projet a été conçu et développé par la LLaMazing Team, une équipe passionnée par l'innovation et l'automatisation des processus. Nous avons mis en place une solution robuste et évolutive pour optimiser la gestion des fiches clients SPL.
