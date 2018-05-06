echo "Installing dependencies..."
pip install --upgrade -r requirements.txt
pip install --upgrade git+git://github.com/LoicEm/PyTorch-Multi-Style-Transfer.git


echo "Downloading model..."
cd backend/
chmod 766 models/download_model.sh
models/download_model.sh
cd ..