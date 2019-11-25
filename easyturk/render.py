"""Script to render a given EasyTurk task.
"""

# -*- coding: utf-8 -*-

import argparse

from easyturk import EasyTurk
import uuid
import json
import random

#from jinja2 import Environment
#from cachelib import SimpleCache

#from django.templatetags.static import static
#from django.urls import reverse

#from django.contrib.staticfiles.storage import staticfiles_storage
#from django.core.urlresolvers import reverse

from interface import configure_guesswhich_tasks
from interface import visualize_guesswhich_task

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', required=True)
    parser.add_argument('--output', required=True)

    #parser.add_argument('--specify_config', action='store_true')
    parser.add_argument('--HIT-config-json', type=str)
    args = parser.parse_args()

    # Compile the template.
    et = EasyTurk()
    env = et.get_jinja_env()
    template = env.get_template(args.template)



    #env2 = Environment(extensions=[FragmentCacheExtension])
    #env2.fragment_cache = SimpleCache()

    '''
    from django.templatetags.static import static
    from django.urls import reverse

    from jinja2 import Environment


    def environment(**options):
        env = Environment(**options)
        env.globals.update({
            'static': static,
            'url': reverse,
        })
        return env
    '''

    '''
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    env2 = et.get_jinja_env()
    env2.globals.update({
            'static':staticfiles_storage.url,
            'url': reverse
        })
    template2 = env2.get_template(args.template)'''


    '''
    socketid = uuid.uuid4()
    class PoolImage:
        """
        Class to store the details related to a particular pool
        """

        def __init__(self, image_path, score, img_id, rank):
            self.image_path = image_path
            self.score = score
            self.img_id = img_id
            self.rank = rank

    intro_message = "Hello I'm a bot. I'm being transparent, don't sue me."
    static_data_dir = "http://web.stanford.edu/~aon2/MeetingOfTheMinds/mturk/static"

    image_pool_json = json.load(open('/Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/pools.json','r'))
    image_pool = image_pool_json[0]

    url_prefix = "http://images.cocodataset.org/val2014/"
    all_images_filenames = json.load(open('/Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/image_filenames_all.json','r'))
        #COCO_val2014_00000013452345.jpg
    all_images_ids = [f_name.replace(".jpg","") for f_name in all_images_filenames]
    all_images_urls = [url_prefix + f_name for f_name in all_images_filenames]

    pool_image_ids_and_target = random.sample(image_pool['pools']['easy']+[image_pool['target']], 20)
    target_image_id = random.choice(pool_image_ids_and_target)
    pool_image_ids = pool_image_ids_and_target[:]
    pool_image_filenames = [im_id + '.jpg' for im_id in pool_image_ids]
    pool_urls = [url_prefix + f_name for f_name in pool_image_filenames]

    image_list = pool_image_ids
    img_list = [PoolImage(pool_urls[i], 0, pool_image_ids[i], i+1) for i in range(len(pool_image_ids))]

    target_filename = target_image_id + '.jpg'
    target_image_url = url_prefix + target_filename
    # Assign 0 rank to all of the images
    scores = [0] * 20
    caption = image_pool['gen_caption']

    translator_type = 'binary'
    answerer_type = 'binary'

    #html = template.render({'input': ''})
    html = template.render({
        "socketid": socketid,
        "bot_intro_message": intro_message,
        "img_list": img_list,
        "target_image": target_image_url,
        "target_image_id": target_image_id,
        "scores": scores,
        "img_id_list": json.dumps(image_list),
        "caption": caption,
        "max_rounds": 9,
        "num_of_games_in_a_hit": 2,
        "disabled": False,
        "total_bonus_so_far": 0,
        "max_game_bonus": 200,
        "bonus_deduction_on_each_click": 20,
        "next_game_id": 0,
        "bonus_for_correct_image_after_each_round": 10,
        "show_feedback_modal": False,
        "static_data_dir": static_data_dir,
        "translator_type": translator_type,
        "answerer_type": answerer_type,
        "pool_index": 0,
        "difficulty_level": "medium",
        })
    '''
    if args.HIT_config_json:
        config = json.load(open(args.HIT_config_json, 'r'))
        task_data = visualize_guesswhich_task(config)
        html = template.render(task_data)

    else:
        all_task_data = configure_guesswhich_tasks(num_hits=1, tasks_per_hit=1, debug=True)
        task_data = all_task_data[0]
        html = template.render(task_data)
   
    # Save to output.
    '''
    chunk_size = 200
    i = 0
    while i < len(html):
        chunk = html[i:i+chunk_size]
        print("chunk = {}".format(chunk))
        print("range = {}--{}".format(i,i+chunk_size))
        str_chunk = str(chunk)
        
        i += chunk_size
    print("Done!")
    '''
    #480-481
    #print("html[480:481] = ", html[480:481])
    #print("html[470:490] = ", html[470:490])
    str_html = html.encode('utf-8')
    with open(args.output, 'w') as f:
        f.write(str_html)
