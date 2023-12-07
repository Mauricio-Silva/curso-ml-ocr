<!-- cspell:disable -->
# Curso de Machine Learning com OCR

Instituto  Federal de Educação, Ciência e Tecnologia de Mato Grosso do Sul - [IFMS](https://www.ifms.edu.br/campi/campus-tres-lagoas)<br/>
Tecnologia em Análise e Desenvolvimento de Sistemas - TADS<br/>

## Tesseract

```bash
# Verifique se você tem o Tesseract instalado:
$ tesseract --version

# Instale o Tesseract para para ler e extrair os textos das imagens
$ sudo apt-get install tesseract-ocr

#  Instale o Tesseract português e espanhol
$ sudo apt-get install tesseract-ocr-por
$ sudo apt-get install tesseract-ocr-spa
```

## Python

```bash
# Verifique se você tem o Python instalado:
$ python3 --version

# Se você NÃO tiver o Python instalado:
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get update
$ sudo apt-get install python3.11
```

## Ambiente Virtual

```bash
# Crie um ambiente virtual dentro da pasta do repositorio
$ python3 -m venv .venv

# Se der erro e/ou você NÂO tiver o venv instalado:
sudo apt-get install -y python3-venv

# Ative o ambiente virtual
$ source .venv/bin/activate

# Verifique se você tem o PIP instalado:
$ pip3 --version

# Se você NÃO tiver o PIP instalado:
$ sudo apt install -y python3-pip
$ sudo python3 -m pip install --upgrade pip
$ pip3 install wheel

# Instale as bibliotecas e pacotes necessários
(.venv) $ pip3 install -r requirements.txt

# Desative o ambiente virtual
$ deactivate
```

## Run

```bash
# Ative o ambiente virtual
$ source .venv/bin/activate

# Execute a aplicação
(.venv) $ python3 app/main.py
```
