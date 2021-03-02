# Market Prediction

### About
This repository contains a submission to the [Market Prediction](https://www.kaggle.com/c/jane-street-market-prediction) competition by [Jane Street](https://www.janestreet.com/) hosted on [Kaggle](https://www.kaggle.com).

### Build
The script [setup.py](setup.py) can be used to build the submission on Kaggle. It assumes that the Kaggle CLI is installed (`pip install kaggle`) and that a valid [API token](https://github.com/Kaggle/kaggle-api) is present. The variable `user` on line 9 needs to be changed to the username corresponding to the API token.

Warning: the notebook [plsxgb.ipynb](notebooks/plsxgb.ipynb) takes ~7 hours to complete on Kaggle because it creates a graphic that is not strictly necessary to construct the model. You may want to delete the corresponding cell (clearly marked in the notebook) in the interest of saving both your time and GPU quota.

### Overview
The [notebooks](notebooks) folder contains the following Jupyter notebooks:
* [eda.ipynb](notebooks/eda.ipynb) explores the data for the competition and identifies a set of important features. It also contains a brief summary of how the competition works.
*  [nn.ipynb](notebooks/nn.ipynb) trains a shallow neural network model.
*  [edaxgb.ipynb](notebooks/edaxgb.ipynb) trains an ensemble of gradient-boosted trees on the subset of features identified by [eda.ipynb](notebooks/eda.ipynb).
*  [plsxgb.ipynb](notebooks/plsxgb.ipynb)  trains an ensemble of gradient-boosted trees on features produced by a partial least squares reduction.
* [tuner.ipynb](notebooks/tuner.ipynb) constructs an ensemble model from  [nn.ipynb](notebooks/nn.ipynb),  [edaxgb.ipynb](notebooks/edaxgb.ipynb), and  [plsxgb.ipynb](notebooks/plsxgb.ipynb) and tunes the weight of each model and the decision threshold based on the validation data.
* [tuned.ipynb](notebooks/tuned.ipynb) contains the code submitted to the competition that makes predictions with the tuned ensemble using Jane Street's API.
* [untuned.ipynb](notebooks/untuned.ipynb) is the same as  [tuned.ipynb](notebooks/tuned.ipynb) but with an ensemble using equal weights of 1/3 and a decision threshold of 1/2.
