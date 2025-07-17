import fitz
import json 

import os
import subprocess

from gen_tocjson import generate_toc_from_images 

def read_json(json_name):
    with open(json_name, 'r') as f: 
        data = json.load(f)
        return data


def extrac_toc_images(toc_pages, file_path, out_name = "aux/toc"): 

    first, last = toc_pages 

    out_name = "aux/toc"

    cmd = ["pdftoppm", "-f", str(first), "-l", str(last),
           file_path, 
           out_name, "-png"] 

    result = subprocess.run(cmd, capture_output=True) 

    print("STDOUT: ", result.stdout)
    print("STDERR", result.stderr)


def apply_toc(json_data):
    offset = json_data["offset"]
    file_path = os.path.expanduser(json_data["file_path"])
    content_page = json_data["toc_pages"][0]

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    doc = fitz.open(file_path)
    max_pages = doc.page_count

    toc = [[1, "Content", content_page]]

    for i, (level, title, page) in enumerate(json_data["toc"]):
        adjusted_page = page + offset 
        if 1 <= adjusted_page <= max_pages:
            toc.append([level, title, adjusted_page])
        else:
            print(f"[⚠] Entrada fuera de rango descartada: '{title}' → página {adjusted_page}")

    doc.set_toc(toc)

    output_path = os.path.join(os.path.dirname(file_path), "TOC_" + os.path.basename(file_path))
    doc.save(output_path)
    doc.close()

    print(f"[✔] TOC aplicado con éxito. Archivo guardado en:\n{output_path}")


#def apply_toc(json_data):
#
#    offset = json_data["offset"]
#    file_path = os.path.expanduser(json_data["file_path"])
#    content_page = json_data["toc_pages"][0]
#
#    toc = [[1, "Content", content_page]] + [
#        [level, title, page + offset] for level, title, page in json_data["toc"]
#    ]
#
#    if not os.path.exists(file_path):
#        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
#
#    doc = fitz.open(file_path)
#    doc.set_toc(toc)
#
#    output_path = os.path.join(os.path.dirname(file_path), "TOC_" + os.path.basename(file_path))
#    doc.save(output_path)
#    doc.close()
#
#    print(f"[✔] TOC aplicado con éxito. Archivo guardado en:\n{output_path}")
#

# Exec commands of terminal. 

if __name__: 


    json_name = "tocs/landau-theory_of_fields.json"
    data = read_json(json_name)

    toc_pages = data["toc_pages"]
    offset = data["offset"] 
    file_path = data["file_path"]
   
    file_path = os.path.expanduser(file_path)

    extrac_toc_images(toc_pages, file_path) 
    

    toc_folder = "aux"
    toc_json_path = f"{toc_folder}/toc.json"

    data["toc"] = read_json(toc_json_path) 
    
    apply_toc(data)
    



