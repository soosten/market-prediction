import json
import os
import subprocess
import tempfile
import time


def main():
    # kaggle username
    user = "soosten"

    # path to the repository from working directory
    path = os.curdir

    # choose an operation
    push_eda_kernel(path, user)
    # push_data(path, user)
    # push_tpu_kernel(path, user)
    # push_utility_kernel(path, user)
    # push_submission_kernel(path, user)

    return


def push_data(path, user):
    kernel = "jane-street-conversion"

    metadata = {"id": user + "/" + kernel,
                "title": "Jane Street - Conversion",
                "code_file": "conversion.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)

    wait_for_kernel(user, kernel)

    metadata = {"id": user + "/jane-street-data",
                "title": "Jane Street - Data",
                "licenses": [{"name": "CC-BY-SA-4.0"}]}

    kernel_to_dataset(user, kernel, metadata)
    return


def push_tpu_kernel(path, user):
    metadata = {"id": user + "/jane-street-tpu",
                "title": "Jane Street - TPU",
                "code_file": "tpu.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "true",
                "dataset_sources": [user + "/jane-street-data"]}

    push_kernel(path, metadata)
    return


def push_utility_kernel(path, user):
    metadata = {"id": user + "/jane-street-utility",
                "title": "Jane Street - Utility",
                "code_file": "utility.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "false",
                "dataset_sources": [user + "/jane-street-data"],
                "kernel_sources": [user + "/jane-street-tpu"]}

    push_kernel(path, metadata)
    return


def push_submission_kernel(path, user):
    metadata = {"id": user + "/jane-street-submission",
                "title": "Jane Street - Submission",
                "code_file": "submission.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "false",
                "enable_gpu": "true",
                "kernel_sources": [user + "/jane-street-tpu",
                                   user + "/jane-street-utility"],
                "dataset_sources": [user + "/jane-street-data"],
                "competition_sources": ["jane-street-market-prediction"]}

    push_kernel(path, metadata)
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


def kernel_to_dataset(user, kernel, metadata):
    with tempfile.TemporaryDirectory() as tempdir:
        # retrive the kernel output
        generation = user + "/" + kernel
        cmd = "kaggle kernels output " + generation + " -p " + tempdir
        subprocess.run(cmd.split())

        # remove the log file
        os.remove(os.path.join(tempdir, kernel + ".log"))

        # write the metadata into appropriate json file
        metafile = os.path.join(tempdir, "dataset-metadata.json")
        with open(metafile, "w") as file:
            json.dump(metadata, file)

        # create dataset using the kaggle command line tool
        cmd = "kaggle datasets create -p " + tempdir
        subprocess.run(cmd.split())

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
