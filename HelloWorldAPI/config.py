# BASE SERVER CONFIGURATION
# General
# use 0.0.0.0:5000 for a docker deployment
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
DEBUG = False
# CORS Configuration
ENABLE_CORS = True  # Activer la conformité CORS uniquement si l'application front est servie par un autre serveur (principalement en configuration dev)
