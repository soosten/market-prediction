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
    # push_eda_kernel(path, user)
    # push_single_kernel(path, user)
    # push_bagging_kernel(path, user)
    # make_tpu_data(path, user)
    push_tpu_kernel(path, user)

    return


def push_bagging_kernel(path, user):
    metadata = {"id": user + "/jane-street-bagging-experiments",
                "title": "Jane Street Bagging Experiments",
                "code_file": "bagging.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "true",
                "competition_sources": ["jane-street-market-prediction"]}
    
    push_kernel(path, metadata)
    return


def push_single_kernel(path, user):
    metadata = {"id": user + "/jane-street-single-time-predictions",
                "title": "Jane Street Single-Time Predictions",
                "code_file": "single-time.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_gpu": "true",
                "enable_internet": "true",
                "competition_sources": ["jane-street-market-prediction"]}
    
    push_kernel(path, metadata)
    return


def push_eda_kernel(path, user):
    metadata = {"id": user + "/jane-street-market-prediction-eda",
                "title": "Jane Street Market Prediction - EDA",
                "code_file": "eda.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "true",
                "competition_sources": ["jane-street-market-prediction"]}
    
    push_kernel(path, metadata)
    return



def push_submission_kernel(path, user):
    metadata = {"id": user + "/jane-street-market-prediction-submission",
                "title": "Jane Street Market Prediction - Submission",
                "code_file": "submission.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "false",
                # "enable_gpu": "true",
                # "kernel_sources": [user + "/model-kernel"]}
                "competition_sources": ["jane-street-market-prediction"]}
    
    push_kernel(path, metadata)
    return


def push_tpu_kernel(path, user):
    metadata = {"id": user + "/jane-street-market-prediction-tpu",
                "title": "Jane Street Market Prediction - TPU",
                "code_file": "tpu.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "true",
                "dataset_sources": [user + "/jane-street-market-prediction-data"]}
    
    push_kernel(path, metadata)
    return


def make_tpu_data(path, user):
    kernel = "jane-street-market-prediction-data-conversion"
    
    metadata = {"id": user + "/" + kernel,
                "title": "Jane Street Market Prediction - Data Conversion",
                "code_file": "conversion.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "competition_sources": ["jane-street-market-prediction"]}
    
    push_kernel(path, metadata)
    
    wait_for_kernel(user, kernel)
    
    metadata = {"id": user + "/jane-street-market-prediction-data",
                "title": "Jane Street Market Prediction - Data",
                "licenses": [{"name": "CC-BY-SA-4.0"}]}
    
    kernel_to_dataset(user, kernel, metadata)
    
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
