"""Delete GuessWhich Tasks
"""

from easyturk import EasyTurk
from easyturk import interface
import json
import os
import argparse
import pdb


def approve_hits(et, hit_ids_to_approve):
	for hit_id in hit_ids_to_approve:
		print("Approving hit {}".format(hit_id))
		et.approve_hit(hit_id)


def main(args):
	use_sandbox = False if args.prod else True
	et = EasyTurk(sandbox=use_sandbox)

	hits_filename = args.json_path
	if os.path.exists(hits_filename):
	    current_hits = json.load(open(hits_filename,'r'))
	    print("Loaded results for {} hits from {}.".format(len(current_hits), hits_filename))

	    progress = et.show_hit_progress(current_hits)
	    print("Retrieved progress for {} hits.".format(len(progress)))
	
	    results = interface.fetch_completed_hits(current_hits, approve=False, sandbox=use_sandbox)
	    print("Loaded results for {} hits from {}. Retrived {} results.".format(len(current_hits), hits_filename, len(results)))
	    if args.breakpoint:
	    	pdb.set_trace()
	    else:
	    	print("Results:\n{}".format(results))
	    	print("Progress:\n{}".format(progress))


	else:
	    print("No hits to review from {}".format(hits_filename))  

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--json-path', type=str, default='launched_hits.json', help='Path to store launched HIT ids.')
	parser.add_argument('--breakpoint', action='store_true', help='break once results loaded for freeform analysis.')
	parser.add_argument('--prod', action='store_true', help='Launch on production AMT, not sandbox.')
	parser.add_argument('--progress', action='store_true', help='Show progress on all the HITs.')
	args = parser.parse_args()
	main(args)
