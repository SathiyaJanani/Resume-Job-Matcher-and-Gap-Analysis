"""Retrain the fit model from recruiter-labeled feature rows."""

import argparse
from src.learned_matcher import train_labeled_model

parser = argparse.ArgumentParser(description="Train the resume fit regressor")
parser.add_argument("csv", help="CSV with semantic,text,skill,experience,evidence,label columns")
args = parser.parse_args()
print(train_labeled_model(args.csv))