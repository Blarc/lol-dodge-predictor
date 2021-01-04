# Using machine learning for predicting League of Legends match outcome

This repository contains the implementation of related article that was written as a part of Machine learning course at
the Faculty of Computer and Information Science at the University of Ljubljana.

## Repository structure

The repository contains the following folders:
- `article` contains the article
- `classifiers` contains implementations of the solutions for the specified problem
- `figs` contains images of plots
- `old` contains old python programs, that were not used in the final implementations
- `prepare_data.py` python program for processing the raw data
- `time_comparison.ipynb` Jupyter Notebook file for comparing classifiers by their learning time and accuracy

## Data

The data set that was used for buliding and testing the models can be accessed [here](https://www.kaggle.com/gyejr95/league-of-legendslol-ranked-games-2020-ver1).

## Reproducing results

To run the Python programs and reproduce the results I got, you will have to download the Kaggle data [set](https://www.kaggle.com/gyejr95/league-of-legendslol-ranked-games-2020-ver1) and extract it to folder `\data\raw_data`.

After you successfully forked this repository and downloaded the data set from Kaggle you will have to install python dependencies listed in `requirements.txt`. You can do this by using pip:
```bash
pip install -r requirements.txt
```

