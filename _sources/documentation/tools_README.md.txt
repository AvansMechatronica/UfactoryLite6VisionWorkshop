# Tools

Hulpprogramma's voor de UFactory Lite 6 vision workshop. Start de scripts vanuit de map `workspace`, met de virtuele omgeving (`.venv`) actief:

```powershell
python tools\<scriptnaam>.py
```

Voor de robotscripts staat het IP-adres in het script (standaard `192.168.1.193`). Pas dit aan naar het adres van jouw robot.

## Robot

### `print_robot_position.py`

Zet de robot in mode 2 (handmatig verplaatsen), state 0, en print elke 0,5 seconde de TCP-positie: `X`, `Y`, `Z` in mm en `roll`, `pitch`, `yaw` in graden. Beweeg de robot met de hand om de waarden te zien veranderen. Druk op een willekeurige toets om te stoppen; de verbinding wordt dan netjes gesloten.

### `print_robot_joints.py`

Hetzelfde als hierboven, maar print de gewrichtshoeken `J1` t/m `J6` in graden. Ook hier stopt het programma met een willekeurige toets.

### `calibrate_workspace.py`

Kalibreert het werkvlak aan de hand van vier markers:

1. De robot gaat naar de home- en observatiepositie en maakt een foto van het werkvlak.
2. Vervolgens gaat de robot in mode 2, zodat je hem met de hand kunt bewegen.
3. Beweeg het kalibratiegereedschap naar marker 1 t/m 4 en druk telkens op Enter om de positie vast te leggen. Tijdens het bewegen verschijnt een waarschuwing als roll/pitch te veel afwijken van 180°/0°.
4. De posities worden opgeslagen in `workspace.json`.

Instellingen bovenin het script: `robot_ip` en `camera_index`.

## Camera

### `captureImage.py`

Maakt foto's met de USB-camera (`camera_index`, standaard 0). Menu:

| Toets | Actie |
|-------|-------|
| `p` | Foto nemen |
| `s` | Laatste foto opslaan (bestandskiezer) |
| `q` | Afsluiten |

### `hsvFilterFromStream.py`

Bepaalt HSV-drempelwaarden op het live camerabeeld. Met de schuifbalken stel je Hue, Saturation en Value (laag/hoog) in; het gefilterde resultaat wordt direct getoond. Met "Revers HUE" kun je rode kleuren filteren, omdat rood aan beide uiteinden van de Hue-schaal ligt. Druk op `q` om te stoppen.

### `hsvFilterFromFile.py`

Zelfde HSV-filter, maar op een afbeelding uit een bestand. Bij het starten kies je een afbeelding. Toetsen:

| Toets | Actie |
|-------|-------|
| `l` | Nieuwe afbeelding laden |
| `q` | Afsluiten |

Sluiten van het filtervenster stopt het programma ook.
