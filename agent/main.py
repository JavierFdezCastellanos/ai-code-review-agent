import os
import sys
import logging
import subprocess
from github_client import GitHubClient
from code_reviewer import CodeReviewer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AICodeReviewAgent:
    def __init__(self, repo_url: str, github_token: str, openai_api_key: str, branch: str = "ai-code-review"):
        self.repo_url = repo_url
        self.github_token = github_token
        self.openai_api_key = openai_api_key
        self.branch = branch
        self.github_client = GitHubClient(repo_url, github_token)
        self.code_reviewer = CodeReviewer(openai_api_key)

    def run(self):
        try:
            logging.info("Iniciando el proceso del agente AI Code Review Agent")
            self.github_client.clone_repo(self.branch)
            
            logging.info("Generando recomendaciones de revisión de código")
            self.code_reviewer.generate_reviews()
            
            logging.info("Realizando push de las recomendaciones generadas")
            self.github_client.push_reviews(self.branch)
            
            logging.info("Creando Pull Request")
            self.github_client.create_pull_request(self.branch)
            
            logging.info("Proceso completado exitosamente.")
        except Exception as e:
            logging.error("Error durante el proceso: %s", str(e))
            sys.exit(1)

def main():
    repo_url = os.getenv("REPO_URL")
    github_token = os.getenv("GITHUB_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not repo_url or not github_token or not openai_api_key:
        logging.error("Faltan variables de entorno necesarias: REPO_URL, GITHUB_TOKEN, OPENAI_API_KEY")
        sys.exit(1)

    agent = AICodeReviewAgent(repo_url, github_token, openai_api_key)
    agent.run()

if __name__ == "__main__":
    main()

