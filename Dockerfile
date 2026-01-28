FROM python:3.12-slim

# Empêche Python de créer des fichiers .pyc et assure un log instantané
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système (nécessaires pour PostgreSQL et autres)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du projet
COPY . .

# On expose le port 8000
EXPOSE 8000

# Commande de lancement (on utilise gunicorn pour la prod)
CMD ["gunicorn", "ecommerce_project.wsgi:application", "--bind", "0.0.0.0:8000"]