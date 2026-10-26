# Voorbeelden

Voorbeeldprogramma's voor de UFactory Lite 6 vision workshop. Start de scripts vanuit de map `workspace`, met de virtuele omgeving (`.venv`) actief:

```powershell
python examples\<scriptnaam>.py
```

Voor de robotvoorbeelden staat het IP-adres in het script (`robot_ip`, standaard `192.168.1.193`) en de camera in `camera_index`. Pas deze aan naar jouw opstelling.

> **Let op:** de robot beweegt zelfstandig naar de home-, observatie- en rustpositie. Zorg dat het werkgebied vrij is en houd de noodstop binnen bereik.

## Robot

### `UFactoryLite6Demo.py`

Eenvoudige demo: de robot beweegt achtereenvolgens naar de home-, linker- en rechterpositie en terug naar home. Daarna wordt de vacuümgripper 2 seconden aangezet (oppakken) en weer uitgezet (loslaten).

### `ServoAngleDemo.py`

Laat zien hoe `robot.set_servo_angle` werkt, met lage snelheid (20°/s): alle zes gewrichten tegelijk (home), één gewricht met `servo_id`, meerdere gewrichten tegelijk, en hoeken in radialen met `is_radian=True`. Daarna worden de huidige hoeken geprint en gaat de robot terug naar home. Zorg dat het werkgebied vrij is.

### `PositionDemo.py`

Laat zien hoe `robot.set_position` werkt, met lage snelheid (50 mm/s): een absolute pose (x, y, z, roll, pitch, yaw), alleen een deel van de waarden wijzigen, relatieve bewegingen met `relative=True` (zijwaarts, omlaag en draaien om yaw) en terug naar de startpose. Na elke stap wordt de positie geprint. Zorg dat het werkgebied vrij is.

## Camera en markers

### `UFactoryCameraTest.py`

Test de combinatie van robot en camera. De robot gaat naar home, naar de observatiepositie, maakt een foto en gaat terug naar home. Daarna kun je via een menu kiezen:

| Toets | Actie |
|-------|-------|
| `o` | Naar observatiepositie (met hulpkruis in het camerabeeld) |
| `r` | Naar rustpositie |
| `p` | Foto nemen en markers tonen |
| `q` | Terug naar home en afsluiten |

### `markerTest.py`

De robot gaat naar de observatiepositie, maakt een foto en gaat terug naar home. In de foto worden de markers van het werkvlak gedetecteerd. Het venster `Crop` toont het uitgesneden werkvlak en `Marker` toont de gedetecteerde markers. Menu: `p` foto nemen, `q` afsluiten.

## Objectherkenning

### `ObjectDetectorTest.py`

Zoals `markerTest.py`, maar op de foto wordt een rood object gezocht met `ObjectDetector` (HSV-filter). Positie, type en kleur van het object worden geprint en het resultaat wordt getoond in het venster `Result`. Menu: `p` foto nemen, `q` afsluiten.

### `SimpleFruits.py`, `SimpleFruitsRoboflow.py`

Fruitherkenning met een model van Roboflow (`simplefruits`) op het livebeeld van de camera. `SimpleFruits.py` stuurt elk beeld naar de Roboflow-webservice en toont het resultaat; `SimpleFruitsRoboflow.py` tekent de gevonden objecten zelf in het beeld. Stoppen kan met een willekeurige toets (met het beeldvenster actief) of door op het kruisje van een venster te klikken. Beide scripts zijn nog niet getest.

### `SimpleFruitsYoloV5.py`

Fruitherkenning met een lokaal YOLOv5-model (`support\SimpleFruitsv1iyolov5pytorch.pt`) op het livebeeld, inclusief weergave van de FPS. Druk op een willekeurige toets (met het beeldvenster actief) of klik op het kruisje van het venster om te stoppen. Dit script is nog niet getest. YOLOv5 moet geïnstalleerd zijn (`yolov5` is aanwezig in de map `workspace`).

> De Roboflow-scripts bevatten een API-sleutel in de code. Zet deze liever in een omgevingsvariabele en deel hem niet.

## Werkvlak

### `WorkspaceTestReletivePose.py`

Leest de kalibratie uit `workspace.json` (gemaakt met `tools\calibrate_workspace.py`) en rekent een positie binnen het werkvlak (x = 0,25, y = 0,25, hoogte 0,2) om naar een robotpositie, die wordt geprint. Het script leest `..\workspace.json`, dus start het vanuit de map `examples`.

## Transformaties en inverse kinematica

### `TransfersAndInverseKinematica\translationinversekinematica.py`

Uitleg-voorbeeld met `pytransform3d` en `ikpy`: transformaties tussen wereld, voetstuk, robot, camera en doos worden opgebouwd en geplot. Daarna worden de gewrichtswaarden berekend met inverse kinematica op basis van `Ned.urdf` (een Niryo Ned-robot, dus niet de Lite 6). Het script moet vanuit zijn eigen map worden gestart, omdat `Ned.urdf` relatief wordt geladen.

## Overige bestanden

| Bestand | Beschrijving |
|---------|--------------|
| `cam_intrinsics.yaml` | Cameraparameters (intrinsics) |
| `support\` | Getraind YOLOv5-model (`.pt` en `.onnx`) voor de fruitherkenning |
