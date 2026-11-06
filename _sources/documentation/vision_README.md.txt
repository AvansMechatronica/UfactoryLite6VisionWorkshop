# Vision-bibliotheek

Functies en klassen voor camerabeeld, markerdetectie, objectherkenning en het omrekenen van beeldposities naar robotposities. Importeer ze vanuit de map `workspace`:

```python
from libraries.vision.usbCamera import usbCamera
from libraries.vision.markers_detection import extract_img_markers, draw_markers
from libraries.vision.ObjectDetector import ObjectDetector
from libraries.vision.Workspace import Workspace
from libraries.vision.enums import *
```

Overzicht van de bestanden:

| Bestand | Inhoud |
|---------|--------|
| [usbCamera.py](./usbCamera.py) | USB-camera met livestream en foto's |
| [markers_detection.py](./markers_detection.py) | Herkennen van de vier werkvlakmarkers |
| [ObjectDetector.py](./ObjectDetector.py) | Objecten zoeken op kleur en vorm |
| [Workspace.py](./Workspace.py) | Werkvlak: relatieve beeldpositie naar robotpositie |
| [image_functions.py](./image_functions.py) | Beeldbewerking, contouren, weergave |
| [CalibrationObject.py](./CalibrationObject.py) | Cameraparameters (intrinsics) |
| [math_functions.py](./math_functions.py) | Hoeken en afstanden |
| [transform_functions.py](./transform_functions.py) | Euler-hoeken, quaternions en matrices |
| [enums.py](./enums.py) | Kleuren, objecttypes en morfologie-instellingen |

---

## usbCamera.py

### `usbCamera(cameraIndex=0, display_stream=True, frame_name="Stream", rotate_frame=False)`

Opent de camera en leest in een aparte thread continu beelden. Is `display_stream` waar, dan wordt het livebeeld in een venster getoond. Met `rotate_frame` wordt het beeld 180° gedraaid.

| Methode | Beschrijving |
|---------|--------------|
| `take_photo(display_photo=True, frame_name="Photo")` | Geeft een kopie van het huidige beeld terug en toont het eventueel |
| `display_photo(frame_name="Photo")` | Toont de laatst genomen foto opnieuw |
| `enable_crosshair(enable)` | Zet een hulpkruis in het midden van de livestream aan of uit (alleen in de weergave, niet in de foto) |
| `set_brightness(waarde)`, `set_contrast(waarde)`, `set_saturation(waarde)` | Bedoeld om helderheid, contrast en verzadiging in te stellen (1.0 = ongewijzigd). **In de huidige code hebben ze geen effect**: ze schrijven naar `_brightness` enz., terwijl het beeld `brightness` enz. gebruikt |
| `end()` | Stopt de thread, sluit de vensters en geeft de camera vrij. Roep dit altijd aan aan het einde |

```python
camera = usbCamera(0)
image = camera.take_photo(display_photo=False)
camera.end()
```

---

## markers_detection.py

Zoekt de vier cirkelvormige markers in de hoeken van het werkvlak. De markers worden gesorteerd als 1 = linksboven, 2 = rechtsboven, 3 = rechtsonder, 4 = linksonder.

| Functie | Beschrijving |
|---------|--------------|
| `extract_img_markers(img, workspace_ratio=1.0)` | Snijdt het werkvlak uit het beeld en rechtt het (perspectief). Geeft `(gelukt, afbeelding)` terug |
| `draw_markers(img, workspace_ratio=1.0)` | Tekent de gevonden markers met nummer in een kopie van het beeld. Geeft `(gelukt, afbeelding)` terug |
| `extract_sub_img(img, list_corners, ratio_w_h=1.0)` | Perspectieftransformatie van vier hoekpunten naar een rechthoekig beeld (korte zijde 400 pixels) |
| `find_markers_from_img_thresh(img_thresh, ...)` | Zoekt markerkandidaten in een zwart-wit beeld |
| `sort_markers_detection(list_markers)` | Sorteert vier markers op positie en oriëntatie |
| `complicated_sort_markers(list_markers, workspace_ratio)` | Kiest de beste vier markers als er 5 of 6 kandidaten zijn |

`workspace_ratio` is de verhouding tussen breedte en hoogte van het werkvlak. Hulpklassen: `PotentialMarker` (enkele cirkel) en `Marker` (samengevoegde cirkels met een identiteit "A" of "B").

> `extract_img_markers` toont ook het venster `Thresholded Image` en print beeldafmetingen.

---

## ObjectDetector.py

### `ObjectDetector(obj_type, obj_color, workspace_ratio=1.0, ret_image_bool=False)`

| Parameter | Betekenis |
|-----------|-----------|
| `obj_type` | `ObjectType.SQUARE`, `ObjectType.CIRCLE` of `ObjectType.ANY` |
| `obj_color` | Kleur uit `ColorHSV` of `ColorHSVPrime`, bijvoorbeeld `ColorHSVPrime.RED` |
| `workspace_ratio` | Breedte/hoogte-verhouding van het werkvlak |
| `ret_image_bool` | Geef een geannoteerd beeld terug |

| Methode | Beschrijving |
|---------|--------------|
| `extract_object_with_hsv(img)` | Volledige pijplijn: werkvlak uitsnijden, kleurfilter, grootste object zoeken. Geeft `(status, pose, objecttype, kleur, beeld)` terug. De positie in `pose.x` en `pose.y` is relatief (0 tot 1) binnen het werkvlak, `pose.yaw` is de hoek |
| `extract_all_object_with_hsv(img, workspace)` | Alle objecten zoeken. **Nog niet geïmplementeerd**: geeft altijd `status = False` |
| `image_preprocess_with_hsv(im_work, use_s_prime=False)` | HSV-drempel gevolgd door een morfologische "open"-bewerking |
| `extract_biggest_blob(im_thresh)` | Zoekt het grootste object en bepaalt middelpunt, hoek, type en kleur (blauw, groen of rood) |
| `relative_pos_from_pixels(x, y)` | Pixelpositie naar relatieve positie (0 tot 1) |
| `get_hsv_parameters()`, `get_img()`, `get_im_thresh()`, `should_ret_image()`, `set_nb_sides(n)` | Hulpmethoden |

Losse functie: `get_annotated_image_rel_pos(img, list_pos, angle, write_on_top=True)` schrijft positie en hoek als tekst in het beeld.

```python
detector = ObjectDetector(ObjectType.ANY, ColorHSVPrime.RED, workspace_ratio=1.0, ret_image_bool=True)
status, pose, obj_type, obj_color, im_draw = detector.extract_object_with_hsv(image)
```

> `extract_object_with_hsv` toont ook het venster `Threshold`.

---

## Workspace.py

### `Workspace()`

Beschrijft het werkvlak met vier robotposities (de markers 1 t/m 4: `UpperLeftPose`, `UpperRightPose`, `LowerRightPose`, `LowerLeftPose`).

| Methode | Beschrijving |
|---------|--------------|
| `set(ul, ur, lr, ll)` | Stelt de vier hoekposen in en berekent breedte, hoogte, oorsprong en hoek |
| `get()` | Geeft de vier hoekposen terug (rechtsboven, linksboven, rechtsonder, linksonder) |
| `to_json()` / `from_json(tekst)` | Opslaan en inlezen van de hoekposen (x, y, z). Dit is het bestand `workspace.json` uit `tools\calibrate_workspace.py` |
| `calculate_parameters()` | Berekent breedte, hoogte, oorsprong (linksboven) en hoek uit de hoekposen |
| `get_pose(x_rel, y_rel, yaw_rel, yaw_center=None)` | Rekent een relatieve positie in het werkvlak (0 tot 1) om naar een robotpose |

```python
workspace = Workspace()
with open("workspace.json") as f:
    workspace.from_json(f.read())
pose = workspace.get_pose(0.25, 0.25, 0.0)
```

> `get_pose` vermenigvuldigt `x_rel` met de hoogte en `y_rel` met de breedte van het werkvlak, en print tussenwaarden. Het `yaw_center`-argument wordt in deze versie niet gebruikt. De z-waarde is het gemiddelde van de vier hoeken.

---

## image_functions.py

**Beeldbewerking**

| Functie | Beschrijving |
|---------|--------------|
| `threshold_hsv(img, min_hsv, max_hsv, reverse_hue=False, use_s_prime=False)` | Zwart-wit masker van pixels binnen het HSV-bereik. `reverse_hue` is nodig voor rood |
| `morphological_transformations(im_thresh, morpho_type, kernel_shape, kernel_type)` | Erode, dilate, open of close op een zwart-wit beeld |
| `undistort_image(img, mtx, dist)` | Corrigeert lensvervorming met cameraparameters |
| `resize_img(img, width=None, height=None, inter=...)` | Schaalt een beeld; geef één maat op om de verhouding te behouden |
| `concat_imgs(tuple_imgs, axis=1)` | Voegt beelden samen (0 = onder elkaar, 1 = naast elkaar) |
| `compress_image(img, quality=90)` / `uncompress_image(data)` | Beeld naar JPEG-bytes (geeft `(gelukt, bytes)`) en terug. Beide gebruiken `tostring`/`fromstring`, die in NumPy 2 niet meer bestaan; hier staat NumPy 2.5 |

**Contouren**

| Functie | Beschrijving |
|---------|--------------|
| `biggest_contours_finder(img, nb_contours_max=3)` | De grootste contouren in een zwart-wit beeld (kleiner dan 400 pixels² wordt genegeerd) |
| `biggest_contour_finder(img)` | De grootste contour |
| `get_contour_barycenter(contour)` | Zwaartepunt `(x, y)` van een contour |
| `get_contour_angle(contour)` | Oriëntatie in radialen, geschikt voor de gripper |
| `draw_contours(img, contours)` | Tekent contouren in een kopie van het beeld |

**Werkvlak en positie**

| Functie | Beschrijving |
|---------|--------------|
| `extract_img_workspace(img, workspace_ratio=1.0)` | Uitgesneden werkvlak op basis van de markers |
| `relative_pos_from_pixels(img, x_pixels, y_pixels)` | Pixelpositie naar relatieve positie (0 tot 1) |

**Weergave**

| Functie | Beschrijving |
|---------|--------------|
| `show_img(window_name, img, wait_ms=1)` | Toont een beeld en geeft de ingedrukte toets terug |
| `show_and_check_close(window_name, img)` | Toont een beeld; geeft `True` bij `q` of Esc |
| `show_and_wait_close(window_name, img)` | Toont een beeld en wacht tot er een toets wordt ingedrukt |
| `add_annotation_to_image(img, text, write_on_top=True)` | Schrijft tekst in het beeld |

**Debug**

| Functie | Beschrijving |
|---------|--------------|
| `debug_threshold_color(img, color_hsv)` | Toont het effect van een kleurfilter |
| `debug_markers(img, workspace_ratio=1.0)` | Zelfde als `draw_markers` |

---

## CalibrationObject.py

### `CalibrationObject(mtx, dist)`

Bevat de cameramatrix (`mtx`) en vervormingscoëfficiënten (`dist`).

| Methode | Beschrijving |
|---------|--------------|
| `set_from_values(mtx, dist)`, `set_from_yaml(yaml)`, `set_empty()` | Aanmaken vanuit waarden, vanuit een ingelezen YAML (`mtx`, `dist`) of leeg |
| `get_intrinsic_parameters()` | `fx`, `fy`, `cx`, `cy` als dictionary |
| `get_center_position()` / `get_center_position_int()` | Beeldmiddelpunt (`cx`, `cy`), eventueel afgerond |
| `get_cam_mtx_and_dist_coefs()`, `get_camera_info()` | De matrix en vervormingscoëfficiënten |
| `undistort_image(img)` | Corrigeert lensvervorming |
| `meters_to_pixels(length, width, z_offset)` | Rekent een afstand in meters om naar pixels op een bepaalde diepte |
| `is_set()` | `True` als de parameters zijn ingevuld |

Een voorbeeld van de parameters staat in `examples\cam_intrinsics.yaml`.

> `set_empty()` gebruikt `np.float`, dat in nieuwe NumPy-versies niet meer bestaat, en geeft dan een fout.

---

## math_functions.py

| Functie | Beschrijving |
|---------|--------------|
| `get_angle_2_points(x1, y1, x2, y2)` | Hoek van de lijn tussen twee punten in radialen |
| `euclidean_dist(x1, y1, x2, y2)` | Afstand tussen twee punten |
| `euclidean_dist_2_pts(p1, p2)` | Afstand tussen twee `(x, y)`-tuples |
| `euclidean_3d_dist(p1, p2)` | 3D-afstand tussen twee objecten met `x`, `y` en `z` |

---

## transform_functions.py

Transformaties tussen hoeken, quaternions en 4×4-matrices (ongewijzigd overgenomen uit de bekende `transformations`-bibliotheek). De standaard hoekvolgorde is `'sxyz'`.

| Functie | Beschrijving |
|---------|--------------|
| `euler_matrix(ai, aj, ak, axes='sxyz')` | Euler-hoeken naar 4×4-rotatiematrix |
| `euler_from_matrix(matrix, axes='sxyz')` | Rotatiematrix naar Euler-hoeken |
| `euler_from_quaternion(quaternion, axes='sxyz')` | Quaternion naar Euler-hoeken |
| `quaternion_matrix(quaternion)` | Quaternion naar 4×4-matrix |
| `quaternion_from_euler(ai, aj, ak, axes='sxyz')` | Euler-hoeken naar quaternion |
| `concatenate_matrices(*matrices)` | Vermenigvuldigt matrices |
| `euclidian_dist(point_a, point_b)` | Afstand tussen twee punten |

---

## enums.py

**Kleuren voor tekst:** `RED`, `PURPLE`, `ORANGE`, `GREEN`, `BLUE`, `WHITE`, `BLACK` (BGR-tuples).

| Klasse | Waarden | Gebruik |
|--------|---------|---------|
| `ColorHSV` | `BLUE`, `RED`, `GREEN`, `ANY` | HSV-bereik: (min, max, hue omkeren) |
| `ColorHSVPrime` | `BLUE`, `RED`, `GREEN`, `ANY` | Bereiken voor het filter met S' = S × V; gebruikt door `ObjectDetector` |
| `ObjectType` | `SQUARE` (4), `CIRCLE` (-1), `ANY` (0) | Vorm van het object |
| `MorphoType` | `ERODE`, `DILATE`, `OPEN`, `CLOSE` | Morfologische bewerking |
| `KernelType` | `RECT`, `ELLIPSE`, `CROSS` | Vorm van de kernel |
| `Command` | `GET_OBJECT_POS`, `GET_OBJECT_RELATIVE_POS` | Commando-ID's |

De HSV-waarden zijn eigenlijk bedoeld voor een Niryo-opstelling. Gebruik de scripts `tools\hsvFilterFromStream.py` en `tools\hsvFilterFromFile.py` om ze op jouw camera en verlichting af te stemmen.
