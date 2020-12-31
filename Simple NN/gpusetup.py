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
    # push_gpu_kernel(path, user)
    wait_for_kernel(user, "jane-street-gpu")
    push_gpuutility_kernel(path, user)
    wait_for_kernel(user, "jane-street-gpu-utility")
    push_gpusubmission_kernel(path, user)
    wait_for_kernel(user, "jane-street-gpu-submission")

    return


def push_gpu_kernel(path, user):
    metadata = {"id": user + "/jane-street-gpu",
                "title": "Jane Street - GPU",
                "code_file": "gpu.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_gpu": "true",
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_gpuutility_kernel(path, user):
    metadata = {"id": user + "/jane-street-gpu-utility",
                "title": "Jane Street - GPU Utility",
                "code_file": "gpuutility.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "false",
                "kernel_sources": [user + "/jane-street-gpu"],
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
    return


def push_gpusubmission_kernel(path, user):
    metadata = {"id": user + "/jane-street-gpu-submission",
                "title": "Jane Street - GPU Submission",
                "code_file": "gpusubmission.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "false",
                "enable_gpu": "true",
                "kernel_sources": [user + "/jane-street-gpu",
                                   user + "/jane-street-gpu-utility"],
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
