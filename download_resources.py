from pathlib import Path
import urllib.request


path_to_model = "resources/Llama-3-8B-Instruct-Gradient-1048k.Q5_K_M.gguf"
link = "https://huggingface.co/PrunaAI/Llama-3-8B-Instruct-Gradient-1048k-GGUF-smashed/resolve/main/Llama-3-8B-Instruct-Gradient-1048k.Q5_K_M.gguf?download=true"

my_file = Path(path_to_model)
if not my_file.is_file():
    print("Model download in progress")
    Path("resources").mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(link, path_to_model)
    print("Model downloaded")
