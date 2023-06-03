# Synergy Httpx
[![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.6-yellow.svg)](https://www.python.org/) 
<img src="https://img.shields.io/badge/Developed%20on-kali%20linux-blueviolet">
[![License](https://img.shields.io/badge/License-BSD-red.svg)](https://github.com/t3l3machus/Synergy-httpx/blob/main/LICENSE.md)
<img src="https://img.shields.io/badge/Maintained%3F-Yes-96c40f">

## Purpose
A Python http(s) server designed to assist in red teaming activities such as receiving intercepted data via POST requests and serving content dynamically (e.g. payloads). 
  
I find this tool handy when working with rubber ducky / bad USB / ATtiny85, etc based attacks. Check out the `ATtiny85_templates` folder for some handy `.ino` templates to load on your microcontroller. Credits: My templates are inspired by this repo -> [CedArctic/DigiSpark-Scripts](https://github.com/CedArctic/DigiSpark-Scripts/).

## Preview


## Installation
```
pip3 install -r requirements.txt
```

## Usage
```
python3 synergy_httpx.py [-h] [-c CERT] [-k KEY] [-p PORT] [-q] [-i INTERFACE]
```  

 - If you provide cert.pem and key.pem files when you execute `synergy_httpx.py`, it will run with SSL. You can use the "serve" and "release" prompt commands to associate server path names with local files to be used as a response body to GET/POST requests, while the server is running.  
  
 - You can predifine endpoints (server paths mapped to local files) by editting the `user_defined_endpoints` dict in `synergy_httpx.py` (there are examples).
