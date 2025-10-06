# Use Python 3.11 as base image
FROM python:3.11

# Add labels metadonnées
LABEL version="1.0"
LABEL maintainer=""
LABEL description=""

# Set working directory
WORKDIR /usr/src/app

# Copy requirements file
COPY requirements.txt .

# Install dependencies without cache car eviter de surcharger les donnée en desactivant le cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . .

# Generate precompiled files (pycache) important pour la portabilité et la performance car cela permet d'éviter la recompilation au demarrage
#les fichiers precompiler les fichier python sont dans limage
RUN python -m compileall .

EXPOSE 5000

# Define entry point
CMD ["python", "HelloWorldAPI.py"]
#ou
#ENTRYPOINT ["python", "HelloWorldAPI.py"]
