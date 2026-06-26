**Manually TO DO:**

# Installing local model.
In you local shell download local LLM first

cd django_boilerplate/models
curl -L -o deepseek.gguf \
https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF/resolve/main/deepseek-coder-6.7b-instruct.Q4_K_M.gguf

NOW --> 'ls -R django_boilerplate/models' should look like this.
################################################
django_boilerplate/models:
  deepseek.gguf	embeddings/

models/embeddings:
  all-MiniLM-L6-v2/

models/embeddings/all-MiniLM-L6-v2:
  1_Pooling/		modules.json		special_tokens_map.json	vocab.txt
  config.json		pytorch_model.bin	tokenizer_config.json

models/embeddings/all-MiniLM-L6-v2/1_Pooling:
  config.json
################################################

**HOW TO SPIN UP THE APP:**
  # Install podman-desktop 
  brew install podman
  brew install --cask podman-desktop
  # Create a new Podman machine
  podman machine init
  # Start the machine
  podman machine start
## OR USE podman-desktop UI app and setup in that application.

python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel
xcode-select --install
brew install cmake

# Build and Run the Pod
podman build -t local-copilot .
podman run -p 8000:8000 -v ./faiss_index:/app/faiss_index local-copilot
##faiss_index is mounted so to avoid create embeddings everytime. But if you change "PROJECT_PATH" in ask_engine.py then 
##you must clear content of ./faiss_index/* before running above command to ensure latest embeddings are created for the new Project.

