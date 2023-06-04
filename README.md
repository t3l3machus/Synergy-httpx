# Synergy Httpx
[![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.6-yellow.svg)](https://www.python.org/) 
<img src="https://img.shields.io/badge/Developed%20on-kali%20linux-blueviolet">
[![License](https://img.shields.io/badge/License-BSD-red.svg)](https://github.com/t3l3machus/Synergy-httpx/blob/main/LICENSE.md)
<img src="https://img.shields.io/badge/Maintained%3F-Yes-96c40f">

## Purpose
A Python http(s) server designed to assist in red teaming activities such as receiving intercepted data via POST requests and serving content dynamically (e.g. payloads). 
  
I find this tool handy when performing USB-based attacks during physical pentests (Rubber ducky / BadUSB / ATtiny85, etc). Check out the `ATtiny85_templates` folder for some handy `.ino` templates to load on your microcontrollers. Credits: My templates are inspired by this repo -> [CedArctic/DigiSpark-Scripts](https://github.com/CedArctic/DigiSpark-Scripts/).

## Preview
![image](https://github.com/t3l3machus/Synergy-httpx/assets/75489922/3d6f49b1-1b2d-44d9-b17a-3c9c41cf9e62)


## Installation
This tool was explicitly developed and tested on kali linux. I doubt it will work properly on Windows.
```
pip3 install -r requirements.txt
```

## Usage
```
python3 synergy_httpx.py [-h] [-c CERT] [-k KEY] [-p PORT] [-q] [-i INTERFACE]
```  

 - If you provide cert.pem and key.pem files when you execute `synergy_httpx.py`, the server will run with SSL (https). 
 - You can use the "serve" and "release" prompt commands to associate/disassociate server path names with local files to be used as a response body to GET/POST requests, while the server is running. There are two standard hardcoded endpoints, 1 x GET mainly for connectivity tests and 1 x POST that will print the request body to the stdout, useful for intercepting data and sending them to your server via http(s).  
 - You can predifine endpoints (server paths mapped to local files) by editting the `user_defined_endpoints` dict in `synergy_httpx.py` (there are examples).
 - Use the "endpoints" prompt command to list all of the server's active endpoints.
