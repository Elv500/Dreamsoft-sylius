import os
from pathlib import Path

def generate_taxon_images_data(file=None, type=None):
    base_dir = Path(__file__).parent.parent / "resources" / "images"

    if file:
        file_path = base_dir / file
    else:
        file_path = base_dir / "test_image_valid.png"
    
    if not file_path.exists():
        raise FileNotFoundError(f"No se encontro el archivo de imagen: {file_path}")
    
    files = {"file": open(file_path, "rb")}
    data = {}
    
    if type:
        data["type"] = type
    
    return files, data