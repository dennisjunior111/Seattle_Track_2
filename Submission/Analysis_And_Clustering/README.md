# HackTheMachine - Redhorse

Repo for utility scripts, notebooks, etc.

**Please do not commit large datasets or dependencies to this repo!**

`/code/simpleInteractionFinder.py` has some utility methods for iterating through AIS data and persisting records of vessels involved in potential interactions. Inputs include distance function and distance threshold.

`/code/AnalyzeInteractionsAndPlot.ipynb` will manually determine interaction pairs, aggregate the timestamped AIS records into a coherent 'fingerprint' of an interaction, and feed these aggregations into a KMeans classifier with k=3 (Meeting Head On, Crossing, Overetaking). The results of this unsupervised classifier are fed into a Decision Tree so the feature_importances can be evaluated.
