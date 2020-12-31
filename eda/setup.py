import json
import os
import subprocess


def main():
    # kaggle username
    user = "soosten"

    # path to the repository from working directory
    path = os.curdir

    # choose an operation
    push_eda_kernel(path, user)

    return


def push_eda_kernel(path, user):
    metadata = {"id": user + "/jane-street-eda",
                "title": "Jane Street - EDA",
                "code_file": "eda.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "true",
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_kernel(path, metadata):
    # write the metadata into appropriate json file
    notebooks = os.path.join(path, "notebooks")
    metafile = os.path.join(notebooks, "kernel-metadata.json")
    with open(metafile, "w") as file:
        json.dump(metadata, file)

    # push using the kaggle command line tool
    cmd = "kaggle kernels push -p " + notebooks
    subprocess.run(cmd.split())

    # remove metadata file
    os.remove(metafile)
    return


if __name__ == "__main__":
    main()
