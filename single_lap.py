""" Bundle segmentation with Rectangular Linear Assignment Problem.

	See Sharmin et al., 'White Matter Tract Segmentation as Multiple 
	Linear Assignment Problems', Fronts. Neurosci., 2017.
"""

import os
import sys
import argparse
import os.path
import ntpath
import nibabel as nib
import numpy as np
from nibabel.streamlines import load
from tractograms_slr import tractograms_slr
from dipy.tracking.streamline import apply_affine
from dissimilarity import compute_dissimilarity, dissimilarity
from dipy.tracking.distances import bundles_distances_mam
from sklearn.neighbors import KDTree
import pickle

try:
    from linear_assignment import LinearAssignment
except ImportError:
    print("WARNING: Cythonized LAPJV not available. Falling back to Python.")
    print("WARNING: See README.txt")
    from linear_assignment_numpy import LinearAssignment


def RLAP(kdt, k, dm_source_tract, source_tract, tractogram, distance):
    """Code for Rectangular Linear Assignment Problem.
    """
    tractogram = np.array(tractogram, dtype=np.object)
    D, I = kdt.query(dm_source_tract, k=k)
    superset = np.unique(I.flat)
    np.save('superset_idx', superset)
    print("Computing the cost matrix (%s x %s) for RLAP... " % (len(source_tract),
                                                             len(superset)))
    cost_matrix = dissimilarity(source_tract, tractogram[superset], distance)
    print("Computing RLAP with LAPJV...")
    assignment = LinearAssignment(cost_matrix).solution
    estimated_bundle_idx = superset[assignment]
    min_cost_values = cost_matrix[np.arange(len(cost_matrix)), assignment]

    return estimated_bundle_idx, min_cost_values


def single_lap(moving_tractogram, static_tractogram, kdt, prototypes, example, k=500, distance_func = bundles_distances_mam):
	"""Code for LAP from a single example.
	"""
	print("Retrieving affine from dictionary.")
	table_filename = 'affine_dictionary.pickle'
	table = pickle.load(open(table_filename))
	moving_tractogram_basename = ntpath.basename(moving_tractogram)
	static_tractogram_basename = ntpath.basename(static_tractogram)
	affine = table[moving_tractogram_basename, static_tractogram_basename].items()[0][1]

	print("Applying the affine to the example bundle.")
	example_bundle = nib.streamlines.load(example)
	example_bundle = example_bundle.streamlines
	example_bundle_aligned = np.array([apply_affine(affine, s) for s in example_bundle])
	
	print("Compute the dissimilarity of the aligned example bundle with the prototypes of target tractogram.")
	example_bundle_aligned = np.array(example_bundle_aligned, dtype=np.object)
	dm_example_bundle_aligned = distance_func(example_bundle_aligned, prototypes)

	print("Segmentation as Rectangular linear Assignment Problem (RLAP).")
	static_tractogram = nib.streamlines.load(static_tractogram)
	static_tractogram = static_tractogram.streamlines
	estimated_bundle_idx, min_cost_values = RLAP(kdt, k, dm_example_bundle_aligned, example_bundle_aligned, static_tractogram, distance_func)
	estimated_bundle = static_tractogram[estimated_bundle_idx]

	return estimated_bundle_idx, min_cost_values, len(example_bundle)


def save_bundle(estimated_bundle_idx, static_tractogram, out_filename):

	extension = os.path.splitext(out_filename)[1]
	static_tractogram = nib.streamlines.load(static_tractogram)
	aff_vox_to_ras = static_tractogram.affine
	voxel_sizes = static_tractogram.header['voxel_sizes']
	dimensions = static_tractogram.header['dimensions']
	static_tractogram = static_tractogram.streamlines
	estimated_bundle = static_tractogram[estimated_bundle_idx]
	
	if extension == '.trk':
		print("Saving bundle in %s" % out_filename)
		
		# Creating header
		hdr = nib.streamlines.trk.TrkFile.create_empty_header()
		hdr['voxel_sizes'] = voxel_sizes
		hdr['voxel_order'] = 'LAS'
		hdr['dimensions'] = dimensions
		hdr['voxel_to_rasmm'] = aff_vox_to_ras 

		# Saving bundle
		t = nib.streamlines.tractogram.Tractogram(estimated_bundle, affine_to_rasmm=np.eye(4))
		nib.streamlines.save(t, out_filename, header=hdr)
		print("Bundle saved in %s" % out_filename)

	elif extension == '.tck':
		print("Saving bundle in %s" % out_filename)

		# Creating header
		hdr = nib.streamlines.tck.TckFile.create_empty_header()
		hdr['voxel_sizes'] = voxel_sizes
		hdr['dimensions'] = dimensions
		hdr['voxel_to_rasmm'] = aff_vox_to_ras

		# Saving bundle
		t = nib.streamlines.tractogram.Tractogram(estimated_bundle, affine_to_rasmm=np.eye(4))
		nib.streamlines.save(t, out_filename, header=hdr)
		print("Bundle saved in %s" % out_filename)

	else:
		print("%s format not supported." % extension)	


if __name__ == '__main__':

	np.random.seed(0) 

	parser = argparse.ArgumentParser()
	parser.add_argument('-moving', nargs='?', const=1, default='',
	                    help='The moving tractogram filename')
	parser.add_argument('-static', nargs='?',  const=1, default='',
	                    help='The static tractogram filename') 
	parser.add_argument('-ex', nargs='?',  const=1, default='',
	                    help='The example (moving) bundle filename')  
	parser.add_argument('-out', nargs='?',  const=1, default='',
	                    help='The output estimated bundle filename')                               
	args = parser.parse_args()

	print("Retrieving kdt and prototypes.")
	kdt_filename='kdt'
	kdt = pickle.load(open(kdt_filename))
	prototypes = np.load('prototypes.npy')

	result_lap = single_lap(args.moving, args.static, kdt, prototypes, args.ex)

	np.save('result_lap', result_lap)

	if args.out:
		estimated_bundle_idx = result_lap[0]
		save_bundle(estimated_bundle_idx, args.static, args.out)

	sys.exit()    

