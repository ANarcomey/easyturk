"""Launch GuessWhich Tasks
"""

from easyturk import EasyTurk
from easyturk import interface
import json
import os
import argparse



def main(args):
	use_sandbox = False if args.prod else True
	hit_ids = interface.launch_guesswhich(num_hits=args.num_hits, reward=args.reward, tasks_per_hit=1, sandbox=use_sandbox)
	print(hit_ids)

	hits_filename = args.json_path
	if not os.path.exists(hits_filename):
		print("Saving generated HITs to {}".format(hits_filename))
		json.dump(hit_ids, open(hits_filename,'w'))
	else:
		print("Adding generated HITs to existing list at {}".format(hits_filename))
		current_hits = json.load(open(hits_filename,'r'))
		all_hits = current_hits + hit_ids
		json.dump(all_hits, open(hits_filename,'w'))


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--json-path', type=str, default='launched_hits.json', help='Path to store launched HIT ids.')
	parser.add_argument('--prod', action='store_true', help='Launch on production AMT, not sandbox.')
	parser.add_argument('--num-hits', type=int, default=10, help='Number of HITs to launch.')
	parser.add_argument('--reward', type=float, default=1.0, help='Reward per HIT.')
	args = parser.parse_args()
	main(args)
