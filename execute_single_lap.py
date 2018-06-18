""" Execute the 3 steps of LAP single example:
1. Registration with SLR
2. Compute dissimilarity and kdtree of the target tractogram
3. Estimate target tract
"""

import os
import sys
import argparse
import os.path
import nibabel as nib
import numpy as np
from nibabel.streamlines import load
from tractograms_slr import tractograms_slr
from compute_kdtree_and_dr_tractogram import compute_kdtree_and_dr_tractogram
from single_lap import single_lap, save_bundle
#from dipy.tracking.streamline import apply_affine

#import pickle

try:
    from linear_assignment import LinearAssignment
except ImportError:
    print("WARNING: Cythonized LAPJV not available. Falling back to Python.")
    print("WARNING: See README.txt")
    from linear_assignment_numpy import LinearAssignment




if __name__ == '__main__':

	np.random.seed(0) 

	parser = argparse.ArgumentParser()
	parser.add_argument('-mov_ID', nargs='?', const=1, default='',
	                    help='The moving subject ID')
	parser.add_argument('-stat_ID', nargs='?',  const=1, default='',
	                    help='The static subject ID') 
	parser.add_argument('-list', nargs='?',  const=1, default='',
	                    help='The tract name list file .txt')                                 
	args = parser.parse_args()

	moving_tractogram_filename = '%s_track.trk' %(args.mov_ID)
	static_tractogram_filename = '%s_track.trk' %(args.stat_ID)

	## Registration with SLR
	affine = tractograms_slr(moving_tractogram_filename, static_tractogram_filename)	

	## Compute dissimilarity and kdtree of the target tractogram
	static_tractogram = nib.streamlines.load(static_tractogram_filename)
	static_tractogram = static_tractogram.streamlines

	kdt, prototypes = compute_kdtree_and_dr_tractogram(static_tractogram)	

	#Saving files
	#kdt_filename='kdt'
	#pickle.dump(kdt, open(kdt_filename, 'w'), protocol=pickle.HIGHEST_PROTOCOL)
	#np.save('prototypes', prototypes)

	## Estimate target tract
	#print("Retrieving kdt and prototypes.")
	#kdt_filename='kdt'
	#kdt = pickle.load(open(kdt_filename))
	#prototypes = np.load('prototypes.npy')
	with open(args.list) as f:
		content = f.read().splitlines()
	
	for t, tract_name in enumerate(content):
		tract_filename = '%s_tract.trk' %(tract_name)
		output_filename = 'tracts_tck/%s_%s_tract_E%s.tck' %(args.stat_ID, tract_name, args.mov_ID)
		result_lap = single_lap(moving_tractogram_filename, static_tractogram_filename, kdt, prototypes, tract_filename)

		#np.save('result_lap', result_lap)
		
		estimated_bundle_idx = result_lap[0]
		save_bundle(estimated_bundle_idx, static_tractogram_filename, output_filename)

	sys.exit()   
