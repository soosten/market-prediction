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



# push_generation_kernel(path, user)
# wait_for_kernel(user, "game-of-life-data-generation")
# generation_kernel_to_dataset(user)
# push_training_kernel(path, user)
# wait_for_kernel(user, "game-of-life-training")
# push_inference_kernel(path, user)
# push_gpu_kernel(path, user)
    
    

def push_gpu_kernel(path, user):
    metadata = {"id": user + "/game-of-life-gpu",
                "title": "Game of Life - GPU",
                "code_file": "gpu.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "true",
                "enable_gpu": "true"}
    
    push_kernel(path, metadata)
    return


def push_deuce(path, user):
    metadata = {"id": user + "/game-of-life-2",
                "title": "Game of Life - 2",
                "code_file": "2level.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "true",
                "enable_gpu": "true"}
    
    push_kernel(path, metadata)
    return


def push_generation_kernel(path, user):
    metadata = {"id": user + "/game-of-life-data-generation",
                "title": "Game of Life - Data Generation",
                "code_file": "generation.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_gpu": "true"}
    
    push_kernel(path, metadata)
    return


def push_training_kernel(path, user):
    metadata = {"id": user + "/game-of-life-training",
                "title": "Game of Life - Training",
                "code_file": "training.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_internet": "true",
                "dataset_sources": [user + "/game-of-life-data"]}
    
    push_kernel(path, metadata)
    return


def push_inference_kernel(path, user):
    metadata = {"id": user + "/game-of-life-inference",
                "title": "Game of Life - Inference",
                "code_file": "inference.ipynb",
                "language": "python",
                "kernel_type": "notebook",
                "enable_gpu": "true",
                "competition_sources": ["conways-reverse-game-of-life-2020"],
                "kernel_sources": [user + "/game-of-life-training"]}
    
    push_kernel(path, metadata)
    return


def generation_kernel_to_dataset(user):
    metadata = {"id": user + "/game-of-life-data",
                "title": "Game of Life - Data",
                "licenses": [{"name": "CC-BY-SA-4.0"}]}

    with tempfile.TemporaryDirectory() as tempdir:
        generation = user + "/game-of-life-data-generation"
        cmd = "kaggle kernels output " + generation + " -p " + tempdir
        subprocess.run(cmd.split())
        
        os.remove(os.path.join(tempdir, "game-of-life-data-generation.log"))
        
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
