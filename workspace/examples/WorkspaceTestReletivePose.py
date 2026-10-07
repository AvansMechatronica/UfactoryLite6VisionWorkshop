from libraries.vision.Workspace import Workspace

workspace = Workspace()

def main():
    with open('../workspace.json') as inputfile:
        workspace.from_json(inputfile.read())

    position = workspace.get_pose(0.25, 0.25, 0.2)
    print(position)

if __name__ == "__main__":
    main()