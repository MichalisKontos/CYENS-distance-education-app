# CYENS-distance-education-app
This application includes an integrated approach for visualizing student activity during distance education

Download the corresponding Unity project at:
https://drive.google.com/drive/folders/19cXXD6ZUKh9xZZbUAcphTpOGwz4wJUMp?usp=sharing

## Install dependencies:
1. Download python from https://www.python.org/downloads/

    • My version used was 3.9.1 (recommended)
    
2. Download pip for python using the following command on a terminal:
```bash
python -m pip install pip
```

3. Use pip to install required packages from requirements.txt:
```bash
pip install -r requirements.txt
```
    or
```bash
python -m pip install -r requirements.txt
```
4. For any issues that may arise with versions of the packages to be installed you can use the following command to install them one by one and with the versions you want (replace “numpy” with the intended package):
```bash
pip install numpy
```
    or
```bash
python -m pip install numpy
```
Note: you can choose what version to install by writing package==version. For example, numpy==1.22.4
5. The needed packages are:

    • numpy
    • onnx
    • onnx-tf
    • opencv-python
    • Pillow

## Run program:

1. To run python files:
```bash
python server.py
```
```bash
python client.py
```
2. Run first the server side and wait for it to start listening and then the client side

3. The client:

    • It will first ask you to choose if you want to run it as a standalone program or along with the server, by typing “a” or “s” respectively.
    
    • If you choose to run it with the server, it will then ask you for an ID to be used for the specific avatar.
    
    • NOTE: No two clients must have the same ID.
