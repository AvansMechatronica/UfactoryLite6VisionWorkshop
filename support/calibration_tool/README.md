# Kalibratiegereedschap

Deze map bevat het 3D-model en printbestanden voor het kalibratiegereedschap van de UFactory Lite 6 Vision Workshop. Met het gereedschap beweeg je de robotpunt naar elk van de vier markers op het werkvlak, zodat de markerposities tijdens de werkvlakkalibratie kunnen worden vastgelegd.

## Bestanden

| Bestand | Beschrijving |
|---|---|
| `calibration_tool.stl` | STL-model om in slicersoftware te openen en zelf een print voor te bereiden. |
| `calibration_tool.3mf` | 3MF-model om in geschikte slicersoftware te openen. |
| `calibration_tool.gcode.3mf` | Bambu Studio-printbestand voor gebruik met een Bambu-printer. |

Volg voor het vastleggen van de vier markerposities de instructies bij `workspace\tools\calibrate_workspace.py` in [`workspace/tools/README.md`](../../workspace/tools/README.md). Controleer voor het printen de schaal en slicerinstellingen. Bevestig het geprinte gereedschap veilig aan de robot voordat je kalibreert.
