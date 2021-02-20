import json
import os
import subprocess
import time


def main():
    # kaggle username
    user = "soosten"

    # path to the repository from working directory
    path = os.curdir

    # EDA
    # push_eda(path, user)

    # models
    push_nn(path, user)
    wait_for_kernel(user, "jane-street-nn")

    push_edaxgb(path, user)
    wait_for_kernel(user, "jane-street-eda-xgb")

    push_plsxgb(path, user)
    wait_for_kernel(user, "jane-street-pls-xgb")

    # tuner
    # push_tuner(path, user)
    # wait_for_kernel(user, "jane-street-tuner")

    # submission
    push_submission(path, user)

    return


def push_eda(path, user):
    metadata = {"id": user + "/jane-street-eda",
                "title": "Jane Street - EDA",
                "code_file": "eda.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_nn(path, user):
    metadata = {"id": user + "/jane-street-nn",
                "title": "Jane Street - NN",
                "code_file": "nn.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_gpu": "true",
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_edaxgb(path, user):
    metadata = {"id": user + "/jane-street-eda-xgb",
                "title": "Jane Street - EDA XGB",
                "code_file": "eda-xgb.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_gpu": "true",
                "enable_internet": "true",
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_plsxgb(path, user):
    metadata = {"id": user + "/jane-street-pls-xgb",
                "title": "Jane Street - PLS XGB",
                "code_file": "pls-xgb.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_gpu": "true",
                "enable_internet": "true",
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_tuner(path, user):
    metadata = {"id": user + "/jane-street-tuner",
                "title": "Jane Street - Tuner",
                "code_file": "tuner.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "false",
                "kernel_sources": [user + "/jane-street-nn",
                                   user + "/jane-street-eda-xgb",
                                   user + "/jane-street-pls-xgb"],
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_submission(path, user):
    metadata = {"id": user + "/jane-street-submission",
                "title": "Jane Street - Submission",
                "code_file": "submission.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "false",
                "enable_gpu": "true",
                "kernel_sources": [user + "/jane-street-nn",
                                   user + "/jane-street-eda-xgb",
                                   user + "/jane-street-pls-xgb",
                                   user + "/jane-street-tuner"],
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


def wait_for_kernel(user, slug, interval=300):
    cmd = "kaggle kernels status " + user + "/" + slug
    output = ""

    # while the status of the kernel is not complete,
    # wait and then check the status of the kernel
    while "complete" not in output:
        print(f"Waiting for {interval} seconds...")
        time.sleep(interval)
        output = subprocess.check_output(cmd.split()).decode()
        print(output, end="")

    return


if __name__ == "__main__":
    main()
