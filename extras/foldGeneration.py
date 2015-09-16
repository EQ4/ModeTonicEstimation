import json
import os
from extras import fileOperations
from sklearn import cross_validation


def stratified_fold(data_dir, n_folds=10, savefile=''):
	modes = fileOperations.getModeNames(data_dir)
	[filepaths, basefolders] = fileOperations.getFileNamesInDir(data_dir, extension='.pitch')[0: 2]

	filemodes = [os.path.basename(b) for b in basefolders]
	mode_idx = [modes.index(m) for m in filemodes]

	# get the stratified folds
	skf = cross_validation.StratifiedKFold(mode_idx, n_folds=n_folds)

	folds = dict()
	for ff, fold in enumerate(skf):
		folds['fold' + str(ff)] = {'train': [], 'test': []}
		for tr_idx in fold[0]:
			folds['fold' + str(ff)]['train'].append({'file': filepaths[tr_idx], 'mode': filemodes[tr_idx]})
		for te_idx in fold[1]:
			folds['fold' + str(ff)]['test'].append({'file': filepaths[te_idx], 'mode': filemodes[te_idx]})

	# save the folds to a file if specified
	if savefile:
		with open(savefile, 'w') as f:
			json.dump(folds, f, indent=2)

	return folds
