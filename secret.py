import os
import sys
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()  # Esto carga las variables definidas en .env

repo_url = os.getenv("REPO_URL")
github_token = os.getenv("GITHUB_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not repo_url or not github_token or not openai_api_key:
	logging.error("Falta definir alguna variable de entorno necesaria: REPO_URL, GITHUB_TOKEN, OPENAI_API_KEY")
	sys.exit(1)
