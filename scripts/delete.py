"""Delete GuessWhich Tasks
"""

from easyturk import EasyTurk
from easyturk import interface
import json
import os
import argparse

def main(args):
	use_sandbox = False if args.prod else True
	et = EasyTurk(sandbox=use_sandbox)
	hits_filename = args.json_path

	if os.path.exists(hits_filename):

	    current_hits = json.load(open(hits_filename,'r'))
	    remaining_hits = []
	    for hit in current_hits:
	        success = et.delete_hit(hit)
	        if not success: remaining_hits.append(hit)
	    json.dump(remaining_hits, open(hits_filename,'w'))
	    print("Remaining hits on {}: \n{}".format(hits_filename, remaining_hits))
	else:
	    print("No hits to delete from {}".format(hits_filename))  

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--json-path', type=str, default='launched_hits.json', help='Path to store launched HIT ids.')
	parser.add_argument('--prod', action='store_true', help='Launch on production AMT, not sandbox.')
	args = parser.parse_args()
	main(args)
