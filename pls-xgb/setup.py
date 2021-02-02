import json
import os
import subprocess
import time


def main():
    # kaggle username
    user = "soosten"

    # path to the repository from working directory
    path = os.curdir

    # choose an operation
    # push_xgb(path, user)
    # wait_for_kernel(user, "js-pls-xgb-training")
    # push_xgb_utility(path, user)
    # wait_for_kernel(user, "js-pls-xgb-utility")
    # push_xgb_submissionl(path, user)
    return


def push_xgb(path, user):
    metadata = {"id": user + "/js-pls-xgb-training",
                "title": "JS - PLS XGB - Training",
                "code_file": "xgb.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_gpu": "true",
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_xgb_utility(path, user):
    metadata = {"id": user + "/js-pls-xgb-utility",
                "title": "JS - PLS XGB - Utility",
                "code_file": "xgbutility.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "kernel_sources": [user + "/js-pls-xgb-training"],
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_xgb_submissionl(path, user):
    metadata = {"id": user + "/js-pls-xgb-submission",
                "title": "JS - PLS XGB - Submission",
                "code_file": "xgbsubmission.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "kernel_sources": [user + "/js-pls-xgb-training",
                                   user + "/js-pls-xgb-utility"],
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def wait_for_kernel(user, slug, interval=300):
    cmd = "kaggle kernels status " + user + "/" + slug
    output = ""

    # while the status of the kernel is not complete,
    # wait and then check the status of the kernel
    while '"complete"' not in output:
        print(f"Waiting for {interval} seconds...")
        time.sleep(interval)
        output = subprocess.check_output(cmd.split()).decode()
        print(output, end="")

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
