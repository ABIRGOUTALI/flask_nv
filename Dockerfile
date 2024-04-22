FROM ubuntu:18.04
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev
# Utilisez une image de base légère

FROM python:3.12.0

# Définir le répertoire de travail dans le conteneur
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier les fichiers requis dans le conteneur
COPY . /app



# Exposer le port sur lequel votre application Flask écoute
EXPOSE 5000

# Commande pour démarrer votre application
CMD ["python", "./app.py"]
