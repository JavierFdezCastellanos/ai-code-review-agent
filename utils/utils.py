import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_generated_code(generated_code: str):
    """
    Limpia el código generado eliminando formateo de markdown,
    como líneas que comienzan con triple backticks.
    """
    lines = generated_code.splitlines()
    # Eliminar la línea inicial si es un bloque markdown (por ejemplo, ```python o ```)
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    # Eliminar la línea final si es triple backticks
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)

def read_source_code():
    """
    Lee los archivos fuente (excluyendo los tests) y retorna una lista de tuplas:
    (ruta_relativa, nombre_archivo, contenido).
    """
    code_files = []
    code_files_dict = {}
    for root, _, files in os.walk("."):
        # Evitar procesar archivos dentro de directorios de tests (tanto 'tests')
        if "tests" in root.split(os.sep):
            continue
        for file in files:
            if file.endswith(".py") and not file.startswith("test_"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, ".")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code_files.append((rel_path, file, f.read()))
                except Exception as e:
                    logging.error("Error al leer el archivo %s: %s", file_path, e)
    return code_files

def cleanup_repo(repo_name):
        """
        Elimina la carpeta del repositorio clonado.
        Antes de eliminar, se asegura de volver al directorio padre en caso de encontrarse dentro del repo.
        """
        try:
            current_dir = os.getcwd()
            # Si el directorio actual es el repositorio clonado, retrocede al directorio padre
            if os.path.basename(current_dir) == repo_name:
                os.chdir("..")
            # Verifica si la carpeta del repositorio existe y la elimina
            if os.path.exists(repo_name):
                shutil.rmtree(repo_name)
                logging.info("Repositorio clonado eliminado exitosamente.")
            else:
                logging.info("No se encontró el repositorio clonado para eliminar.")
        except Exception as e:
            logging.error("Error al eliminar el repositorio clonado: %s", e)