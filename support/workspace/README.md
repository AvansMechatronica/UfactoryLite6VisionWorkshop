# Robot vision workspaces

Deze map bevat tekeningen van de workspaces voor de UFactory Lite 6 Vision Workshop. Elk werkvlak heeft vier markers die worden gebruikt om het werkvlak ten opzichte van de robot te kalibreren.

Er zijn twee uitvoeringen:

| Tekening | PDF | Visio |
|---|---|---|
| Workspace voor de stenenmuur | `RobotVisionWorkspaceBricks2Wall.pdf` | `RobotVisionWorkspaceBricks2Wall.vsdx` |
| Workspace V2 | `RobotVisionWorkspaceV2.pdf` | `RobotVisionWorkspaceV2.vsdx` |

Gebruik de PDF-bestanden als referentie voor het maken of opbouwen van een werkvlak. De VSDX-bestanden kunnen in Microsoft Visio worden geopend en bewerkt. Na het plaatsen van de vier markers kan het werkvlak met `workspace\tools\calibrate_workspace.py` worden gekalibreerd; zie de README in `workspace\tools` voor de werkwijze.
