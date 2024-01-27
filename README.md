# Centros de Adultos Mayores y Envejecientes

### Setting up in Windows systems

```sh
# Navigate to project directory
cd path\to\project

# Install virtualenv 
pip install virtualenv

# Create virtual env named 'sdoh'
python -m venv adsef

# Activate the virtual environment 
.\adsef\Script\activate

# Upgrade pip 
python.exe -m pip install --upgrade pip

# Install packages
pip install -r requirements.txt
```

### Setting up in UNIX systems
```bash
# Navigate to project directory
cd /path/to/project

# Install virtualenv 
sudo pip install virtualenv 

# Create virtual env named 'adsef'
python3 -m venv adsef

# Activate the virtual environment 
source adsef/bin/activate

# Upgrade pip 
pip install --upgrade pip

# Install packages
pip install -r requirements.txt
```

### Running the app
```sh
streamlit run path\to\file\a.py
```
