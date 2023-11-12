# TECH TEST


The play_score.py script selects the combination of measures with the highest coverage score (included in the given budget) and plays it against the server. It prints the obtained score or the server response in case of error.

## Tech stack

Python 3.7+ required. Python 3.10 used to build the project.

## Installation and running

### 1) Clone the Test Tenacy repository
```
git clone https://github.com/LaTinaLoca/tech_test_tenacy.git
cd tech_test_tenacy
```

### 2) Create a virtual environment
```
python3 -m venv venv
```

### 3) Activate the virtual environment

#### Linux / Mac
```
source venv/bin/activate
```

#### Windows
```
venv\Scripts\activate
```
 
### 4) From the virtual env prompt, install the required packages
```
pip install -r requirements.txt
```

### 5) Update the AUTHENTICATION_TOKEN parameter in config.py file to be able to shoot request to the test server


### 6) Run the play_score script
```
python play_score.py
```

### 7) unittests can be run using
```
 python -m unittest discover
```



