# 📦 E-Commerce Project (Version Monolithique)

Ce dépôt contient la version **monolithique** de l'application e-commerce. C'est une application Django complète où toutes les fonctionnalités (Catalogue, Commandes, Auth) sont regroupées dans une seule unité de déploiement.

## 🛠️ Stack Technique
- **Framework** : Django 6.0.1
- **Interface Admin** : Django Jazzmin (Dashboard moderne)
- **Serveur de Production** : Gunicorn
- **Gestion des Statiques** : WhiteNoise
- **Conteneurisation** : Docker & Docker Compose

## 🧐 Pourquoi cette version ?
Cette application a servi de base pour la transition vers une architecture **microservices**. Elle permet de démontrer :
1. La simplicité de développement d'un monolithe.
2. Les limites en termes de scalabilité et de résilience (si le serveur tombe, tout le site tombe).

## 🚀 Installation et Lancement

### Avec Docker (Recommandé)
```bash
# 1. Construire et lancer le conteneur
docker-compose up -d --build

# 2. Appliquer les migrations
docker-compose exec web python manage.py migrate

# 3. Créer un accès admin
docker-compose exec web python manage.py createsuperuser