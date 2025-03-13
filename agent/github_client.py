import os
import subprocess
import logging
import github3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GitHubClient:
    def __init__(self, repo_url: str, token: str):
        #self.repo_url = repo_url
        self.repo_url = repo_url.replace("https://", f"https://{token}@")
        self.token = token
        self.user, self.repo_name = self._parse_repo_url(repo_url)

    def _parse_repo_url(self, repo_url: str):
        parts = repo_url.rstrip('/').split('/')
        try:
            user = parts[-2]
            repo_name = parts[-1].replace(".git", "")
            return user, repo_name
        except IndexError:
            raise ValueError("La URL del repositorio es inválida.")

    def clone_repo(self, branch: str):
        logging.info("Clonando el repositorio %s...", self.repo_url)
        try:
            subprocess.run(["git", "clone", self.repo_url], check=True)
            os.chdir(self.repo_name)
            if branch=="ai-code-review":
                subprocess.run(["git", "checkout", "-b", branch], check=True)
            else:
                subprocess.run(["git", "checkout", branch], check=True)
                subprocess.run(["git", "pull", "origin", branch], check=True)
        except subprocess.CalledProcessError as e:
            logging.error("Error al clonar o crear la rama: %s", e)
            raise

    def push_reviews(self, branch: str):
        logging.info("Haciendo push de las recomendaciones en la rama %s...", branch)
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "AI-generated code review recommendations"], check=True)
            subprocess.run(["git", "push", "origin", branch], check=True)
        except subprocess.CalledProcessError as e:
            logging.error("Error al hacer push de las recomendaciones: %s", e)
            raise

    def create_pull_request(self, branch: str):
        logging.info("Creando Pull Request para la rama %s...", branch)
        gh = github3.login(token=self.token)
        repo = gh.repository(self.user, self.repo_name)
        if not repo:
            raise ValueError("Repositorio no encontrado. Verifica la URL y los permisos.")
        pr = repo.create_pull(
            title="AI-generated code review recommendations",
            base="development",
            head=branch,
            body="Estas recomendaciones fueron generadas automáticamente por IA."
        )
        if pr:
            logging.info("Pull Request creado exitosamente: %s", pr.html_url)
        else:
            logging.error("Error al crear el Pull Request.")

