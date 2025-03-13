import os
import sys
import logging
import secret
from agent.github_client import GitHubClient
from agent.code_reviewer import CodeReviewer
from utils.utils import cleanup_repo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AICodeReviewAgent:
    def __init__(self, repo_url: str, github_token: str, openai_api_key: str, branch: str):
        self.repo_url = repo_url
        self.github_token = github_token
        self.openai_api_key = openai_api_key
        self.branch = branch
        self.github_client = GitHubClient(repo_url, github_token)
        self.repo_name = self.github_client._parse_repo_url(repo_url)[1]
        self.code_reviewer = CodeReviewer(openai_api_key)

    def run(self):
        try:
            logging.info("Iniciando el proceso del agente AI Code Review Agent")
            self.github_client.clone_repo(self.branch)
            
            logging.info("Generando recomendaciones de revisión de código")
            self.code_reviewer.run()
            
            logging.info("Realizando push de las recomendaciones generadas")
            self.github_client.push_reviews(self.branch)
            
            logging.info("Creando Pull Request")
            self.github_client.create_pull_request(self.branch)
            
            logging.info(f"Eliminando el repositorio: {self.repo_name}")
            cleanup_repo(self.repo_name)
            
            logging.info("Proceso completado exitosamente.")
        except Exception as e:
            logging.error("Error durante el proceso: %s", str(e))
            sys.exit(1)

def main():
    repo_url = os.getenv("REPO_URL")
    github_token = os.getenv("GITHUB_TOKEN")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    branch_name = "ai-code-review"
    print(sys.argv)
    print(len(sys.argv))
    if len(sys.argv) > 2:
        branch_name = sys.argv[1]
        print(branch_name)


    agent = AICodeReviewAgent(repo_url, github_token, openai_api_key, branch_name)
    agent.run()

if __name__ == "__main__":
    main()

