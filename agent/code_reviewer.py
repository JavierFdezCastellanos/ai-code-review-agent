import os
import openai
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_generated_text(generated_text: str) -> str:
    """
    Limpia el texto generado eliminando formateo de markdown, como líneas que comienzan o terminan con triple backticks.
    """
    lines = generated_text.splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)

class CodeReviewer:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def read_source_code(self):
        """
        Lee los archivos fuente (excluyendo los archivos de test y el directorio reviews)
        y retorna una lista de tuplas (nombre, contenido).
        """
        code_files = []
        for root, _, files in os.walk("."):
            # Evitar procesar archivos dentro del directorio 'reviews'
            if "reviews" in root.split(os.sep):
                continue
            for file in files:
                if file.endswith(".py") and not file.startswith("test_"):
                    file_path = os.path.join(root, file)
                    # Omitir __init__.py
                    if file == "__init__.py":
                        continue
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            code_files.append((file, f.read()))
                    except Exception as e:
                        logging.error("Error al leer el archivo %s: %s", file_path, e)
        return code_files

    def generate_reviews(self):
        """
        Genera recomendaciones de mejora para cada archivo fuente utilizando la API de OpenAI.
        Guarda las recomendaciones en archivos dentro del directorio 'reviews'.
        """
        if not self.api_key:
            raise EnvironmentError("La variable de entorno OPENAI_API_KEY no está definida.")

        code_snippets = self.read_source_code()
        if not code_snippets:
            logging.warning("No se encontraron archivos fuente para revisar.")
            return

        os.makedirs("reviews", exist_ok=True)
        
        for filename, code in code_snippets:
            review_filename = os.path.join("reviews", f"review_{filename}.md")
            prompt = (
                "Revisa el siguiente código Python y proporciona recomendaciones de mejora, "
                "incluyendo refactorizaciones, optimizaciones y mejoras en el estilo. "
                "Devuelve solo las recomendaciones en formato markdown, sin explicaciones adicionales.\n\n"
                f"{code}\n\n"
            )
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un experto en revisión de código."},
                        {"role": "user", "content": prompt}
                    ],
                    api_key=self.api_key
                )
                review_text = response["choices"][0]["message"]["content"]
                review_text = clean_generated_text(review_text)
                with open(review_filename, "w", encoding="utf-8") as f:
                    f.write(review_text)
                logging.info("Revisión generada para %s y guardada en %s", filename, review_filename)
            except Exception as e:
                logging.error("Error al generar la revisión para %s: %s", filename, e)
        logging.info("Todas las recomendaciones han sido generadas en el directorio 'reviews'.")

