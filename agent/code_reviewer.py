import openai
import logging
from utils.utils import clean_generated_code, read_source_code

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CodeReviewer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def run(self):
        if not self.api_key:
            raise EnvironmentError("La variable de entorno OPENAI_API_KEY no está definida.")
        
        code_snippets = read_source_code()
        
        if not code_snippets:
            logging.warning("No se encontraron archivos fuente para generar tests.")
            return

        for rel_path, file_name, code in code_snippets:
            # Omitir archivos que no se desean procesar
            if file_name in ['__init__.py']:
                logging.info(f"No se generan tests para el archivo {file_name}")
                continue
            self.generate_reviews(rel_path, file_name, code)
            
        logging.info("Todas las recomendaciones han sido generadas en el directorio 'reviews'.")


    def generate_reviews(self, rel_path, file_name, code):
        """
        Genera recomendaciones de mejora para cada archivo fuente utilizando la API de OpenAI.
        Guarda las recomendaciones en archivos dentro del directorio 'reviews'.
        """
    
        prompt = (
            "Revisa el siguiente código Python y Mejoralo" 
            "incluyendo refactorizaciones, optimizaciones y mejoras en el estilo. "
            "Devuelve solo el codigo, sin explicaciones adicionales.\n\n"
            f"{code}\n\n"
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto Senior Data Engineer."},
                    {"role": "user", "content": prompt}
                ],
                api_key=self.api_key
            )
            review_text = response["choices"][0]["message"]["content"]
            review_text = clean_generated_code(review_text)
            with open(rel_path, "w", encoding="utf-8") as f:
                f.write(review_text)
            logging.info("Revisión generada para %s y guardada en %s", file_name, rel_path)
        except Exception as e:
            logging.error("Error al generar la revisión para %s: %s", file_name, e)
        

