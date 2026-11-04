# Workspace Vision Driven Robotics

Deze map bevat de Python-code voor de UFactory Lite 6 Vision Workshop: robot- en camerademo's, vision- en pick-and-placevoorbeelden, kalibratietools en ondersteunende bestanden.

## Mappen en bestanden

| Pad | Inhoud |
|---|---|
| `examples\` | Voorbeelden voor de robot, camera, objectherkenning, pick-and-place en transformaties. |
| `tools\` | Hulpprogramma's voor werkvlakkalibratie, camerabeelden, HSV-filters en het uitlezen van robotposities. |
| `libraries\` | Map voor gedeelde workshopcode. |
| `Images\` | Afbeeldingen voor gebruik bij de voorbeelden. |
| `yolov5\` | YOLOv5-code voor lokale objectherkenning. |
| `workspace.json` | Kalibratieposes van de vier hoeken van het werkvlak. |
| `requirements.txt` | Python-afhankelijkheden voor de workspace. |

De voorbeelden en tools hebben aanvullende uitleg in [`examples\README.md`](examples/README.md) en [`tools\README.md`](tools/README.md).

## Installatie

Gebruik Python 3.12 en voer de volgende opdrachten uit in PowerShell vanuit deze map:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

In VS Code kun je `.venv` als Python-interpreter selecteren. Zie ook de workshopinstructies voor [software-installatie](../documentation/documentation/install.md).

## Voorbeelden uitvoeren

Voer scripts vanuit de map `workspace` uit, met de virtuele omgeving geactiveerd. Bijvoorbeeld:

```powershell
python examples\UFactoryLite6Demo.py
python tools\captureImage.py
```

Controleer bij robotvoorbeelden vooraf de ingestelde `robot_ip` en bij cameravoorbeelden de `camera_index`. Sommige voorbeelden bewegen de robot zelfstandig. Houd het werkgebied vrij en zorg dat de noodstop bereikbaar is.

Voor aansluiting en netwerkconfiguratie van de robot, zie de instructies voor het [klaarzetten van de robot](../documentation/documentation/setup.md).
