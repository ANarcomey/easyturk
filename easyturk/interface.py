"""Functions to launch, retrieve, and parse specific EasyTurk tasks.
"""

from easyturk import EasyTurk
import random
import json


def launch_verify_question_answer(data, reward=1.00, tasks_per_hit=50, sandbox=False):
    """Launches HITs to ask workers to verify bounding boxes.

    Args:
        data: List containing image urls, questions and answers, for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'verify_question_answer.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit = et.launch_hit(
            template, data[i:i+tasks_per_hit], reward=reward,
            title='Verify the answer to a question about an picture',
            description=('Verify whether an answer to a question about a picture is correct.'),
            keywords='image, text, picture, answer, question, relationship')
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def launch_verify_relationship(data, reward=1.00, tasks_per_hit=30, sandbox=False):
    """Launches HITs to ask workers to verify bounding boxes.

    Args:
        data: List containing image urls, relationships, for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'verify_relationship.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit = et.launch_hit(
            template, data[i:i+tasks_per_hit], reward=reward,
            title='Verify relationships between objects in pictures',
            description=('Verify whether the relationships are correctly identified in pictures.'),
            keywords='image, text, picture, object, bounding box, relationship')
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def launch_verify_bbox(data, reward=1.00, tasks_per_hit=30, sandbox=False):
    """Launches HITs to ask workers to verify bounding boxes.

    Args:
        data: List containing image urls, objects, for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'verify_bbox.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit = et.launch_hit(
            template, data[i:i+tasks_per_hit], reward=reward,
            title='Verify objects in pictures',
            description=('Verify whether objects are correctly identified in pictures.'),
            keywords='image, text, picture, object, bounding box')
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def launch_caption(data, reward=1.00, tasks_per_hit=10, sandbox=False):
    """Launches HITs to ask workers to caption images.

    Args:
        data: List containing image urls for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'write_caption.html'
    hit_ids = []
    i = 0
    while i < len(data):
        hit = et.launch_hit(
            template, data[i:i+tasks_per_hit], reward=reward,
            title='Caption some pictures',
            description=('Write captions about the contents of images.'),
            keywords='image, caption, text')
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def launch_guesswhich(num_hits, reward=1.00, tasks_per_hit=10, sandbox=False):
    """Launches HITs to ask workers to caption images.

    Args:
        data: List containing image urls for the task.
        reward: A postive valued dollar amount per task.
        tasks_per_hit: Number of images per hit.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A list of hit ids that have been launched.
    """
    et = EasyTurk(sandbox=sandbox)
    template = 'guesswhich/index_et.html'
    hit_ids = []
    all_task_data = configure_guesswhich_tasks(num_hits, tasks_per_hit, debug=False)
    i = 0
    while i < len(all_task_data):
        hit = et.launch_hit_unicode(
            #template, all_task_data[i:i+tasks_per_hit], reward=reward,
            template, all_task_data[i:i+tasks_per_hit][0], reward=reward,
            title='Guess Which game with chatbot',
            description=('Play interactive \'Guess Which\' image guessing game with a chatbot.'),
            keywords='image, questions, chatbot, guessing',
            frame_height=0)
        hit_id = hit['HIT']['HITId']
        hit_ids.append(hit_id)
        i += tasks_per_hit
    return hit_ids


def configure_guesswhich_tasks(num_hits, tasks_per_hit=10, debug=False):
    class PoolImage:
        """
        Class to store the details related to a particular pool
        """
        def __init__(self, image_path, score, img_id, rank):
            self.image_path = image_path
            self.score = score
            self.img_id = img_id
            self.rank = rank


    # constants and filenames
    '''
    intro_message = "Hello, I'm a question answering bot." \
                    " I have been assigned one of these images as the target image." \
                    " I am not allowed to show you the image, but you can ask me questions about the target image." \
                    " After each question you ask, choose your best guess of which image is the target." \
                    " You will win extra bonuses based on how accurately you can guess the target image." \
                    " I am not perfect, but we can work together to find the target image!"
    '''
    intro_message = ["Hello, I'm a question answering bot here to play a collaborative guessing game!" \
                    " <b>I have been secretly assigned one of the images on the left</b>, and I am not allowed to show you the image," \
                    " but you can ask me 9 questions about this image. Use these questions to narrow down which is my image." \
                    " After each question you ask, choose your best guess of which image is my secret image.", \
                    " <b>Accurate guessing will win you bonuses!</b>" \
                    " Each game pays <b>$1.00</b>, and you will win an additional <b>$0.10</b> for each correct guess during the 9 questions." \
                    " Once we've completed 9 questions, you will guess until you find my secret image. You can get bonus here too!"
                    " This additional bonus starts at <b>$0.30</b> and decreases by <b>$0.05</b> with each incorrect guess, but you can't lose base payment or the other bonuses!", \
                    " I am not perfect, but we can work together to find the secret image!" \
                    " <b>Ask your first question now!</b>"]

    static_data_dir_local = "file:///Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/static"
    static_data_dir_web = "https://web.stanford.edu/~aon2/MeetingOfTheMinds/mturk/static"
    url_prefix = "http://images.cocodataset.org/val2014/"
    image_pool_json_filename = '/Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/pools.json'
    all_images_filenames_filename = '/Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/image_filenames_all.json'
    categories_json_filename = '/Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/categories.json'
    post_endpoint = "https://visualgenome.org/hits/guess_which"
    get_endpoint = "https://visualgenome.org/hits/get_guess_which_results"

    
    # configurations
    static_data_dir = static_data_dir_web #static_data_dir_local
    difficulty_level = "easy"
    max_rounds = 9#9
    num_ims_in_pool = 20
    starting_final_bonus = 0.30#200
    bonus_deduction_on_each_click = 0.05#20
    bonus_for_correct_image_after_each_round = 0.10#20
    base_payment = 1.0
    if debug: #set constants to run short debugging version of game
        max_rounds = 3
        debug_show_answer = True
        debug_logging = True
    else:
        debug_show_answer = False
        debug_logging = False

    # study configuration
    study_name = "pilot_allcats_no_translator" # CHANGE THIS VARIABLE TO RUN DIFFERENT STUDIES

    if study_name == "pilot_binary_no_translator":
        study_type = "no_translator" # choose "no_translator" | "translator_show_answer" | "translator_ask_show_answer"
        study_description = "Pilot study with binary answerer, no translator (binary chosen to satisfy server but hidden from user)."
        randomize_pool_index = True
        randomize_answerer_type = False
        default_answerer_type = "binary"
        default_translator_type = "binary"
        print("Configuring {} HITS for {} study. Description:\n{}".format(num_hits, study_name, study_description))
    elif study_name == "pilot_allcats_no_translator":
        study_type = "no_translator" # choose "no_translator" | "translator_show_answer" | "translator_ask_show_answer"
        study_description = "Pilot study with all-category answerer, no translator (all-category chosen to satisfy server but hidden from user)."
        randomize_pool_index = True
        randomize_answerer_type = False
        default_answerer_type = "all_categories"
        default_translator_type = "all_categories"
        print("Configuring {} HITS for {} study. Description:\n{}".format(num_hits, study_name, study_description))
    else:
        raise ValueError("Study of name {} not currently supported.".format(study_name))


    # load
    image_pool_json = json.load(open(image_pool_json_filename,'r'))
    all_images_filenames = json.load(open(all_images_filenames_filename,'r'))
    categories = json.load(open(categories_json_filename,'r'))

    all_task_data = []
    for i in range(num_hits):
        for j in range(tasks_per_hit):
            # randomly determined parameters
            pool_index = random.choice(range(len(image_pool_json))) if randomize_pool_index else 4

            if study_type == "no_translator":
                translator_type = default_translator_type
                answerer_type = random.choice(categories) if randomize_answerer_type else default_answerer_type
            elif study_type == "translator_show_answer" or study_type == "translator_ask_show_answer":
                #TODO
                pass
            else:
                raise ValueError("Invalid study configuration.")

            image_pool = image_pool_json[pool_index]

            #pool_image_ids_and_target = random.sample(image_pool['pools'][difficulty_level]+[image_pool['target']], num_ims_in_pool)
            pool_image_ids_and_target = random.sample(image_pool['pools'][difficulty_level], num_ims_in_pool)
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

            task_data = {
                "post_endpoint": post_endpoint,
                "get_endpoint": get_endpoint,
                "bot_intro_message": intro_message,
                "img_list": img_list,
                "target_image": target_image_url,
                "target_image_id": target_image_id,
                "scores": scores,
                "img_id_list": json.dumps(image_list),
                "caption": caption,
                "max_rounds": max_rounds,
                "num_of_games_in_a_hit": tasks_per_hit,
                "disabled": False,
                "total_bonus_so_far": 0,
                "starting_final_bonus": starting_final_bonus,
                "bonus_deduction_on_each_click": bonus_deduction_on_each_click,
                "base_payment": base_payment,
                "next_game_id": j,
                "bonus_for_correct_image_after_each_round": bonus_for_correct_image_after_each_round,
                "show_feedback_modal": False,
                "static_data_dir": static_data_dir,
                "translator_type": translator_type,
                "answerer_type": answerer_type,
                "pool_index": pool_index,
                "difficulty_level": difficulty_level,
                "study_type": study_type,
                "study_description": study_description,
                "debug_show_answer": debug_show_answer,
                "debug_logging": debug_logging
            }
            all_task_data.append(task_data)

    return all_task_data


def visualize_guesswhich_task(config):
    class PoolImage:
        """
        Class to store the details related to a particular pool
        """
        def __init__(self, image_path, score, img_id, rank):
            self.image_path = image_path
            self.score = score
            self.img_id = img_id
            self.rank = rank


    # constants and filenames
    '''
    intro_message = "Hello, I'm a question answering bot." \
                    " I have been assigned one of these images as the target image." \
                    " I am not allowed to show you the image, but you can ask me questions about the target image." \
                    " After each question you ask, choose your best guess of which image is the target." \
                    " You will win extra bonuses based on how accurately you can guess the target image." \
                    " I am not perfect, but we can work together to find the target image!"
    '''
    intro_message = ["Hello, I'm a question answering bot here to play a collaborative guessing game!" \
                    " <b>I have been secretly assigned one of the images on the left</b>, and I am not allowed to show you the image," \
                    " but you can ask me 9 questions about this image. Use these questions to narrow down which is my image." \
                    " After each question you ask, choose your best guess of which image is my secret image.", \
                    " <b>Accurate guessing will win you bonuses!</b>" \
                    " Each game pays <b>$1.00</b>, and you will win an additional <b>$0.10</b> for each correct guess during the 9 questions." \
                    " Once we've completed 9 questions, you will guess until you find my secret image. You can get bonus here too!"
                    " This additional bonus starts at <b>$0.30</b> and decreases by <b>$0.05</b> with each incorrect guess, but you can't lose base payment or the other bonuses!", \
                    " I am not perfect, but we can work together to find the secret image!" \
                    " <b>Ask your first question now!</b>"]

    static_data_dir_local = "file:///Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/static"
    static_data_dir_web = "https://web.stanford.edu/~aon2/MeetingOfTheMinds/mturk/static"
    url_prefix = "http://images.cocodataset.org/val2014/"
    image_pool_json_filename = '/Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/pools.json'
    all_images_filenames_filename = '/Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/image_filenames_all.json'
    categories_json_filename = '/Users/austinnarcomey/Documents/Stanford/Research/frontend/GuessWhich_data/categories.json'
    post_endpoint = "https://visualgenome.org/hits/guess_which"
    get_endpoint = "https://visualgenome.org/hits/get_guess_which_results"

    # configurations
    static_data_dir = static_data_dir_web #static_data_dir_local
    max_rounds = 9#9
    num_ims_in_pool = 20
    starting_final_bonus = 0.30#200
    bonus_deduction_on_each_click = 0.05#20
    bonus_for_correct_image_after_each_round = 0.10#20
    base_payment = 1.0

    # Load this specific HIT
    # Inputs
    difficulty_level = config['difficulty_level']
    pool_index = int(config['pool_index'])
    target_image_id = config['target_image_id']

    # Outcomes
    dialog_history = config['dialog_history']
    image_selections = config['image_selections']
    final_image_list = config['final_image_list']
    current_in_game_bonus = config['current_in_game_bonus']
    current_finalround_bonus = config['current_finalround_bonus']
    total_payment = config['total_payment']
    outcome_config_params = ['dialog_history','image_selections','final_image_list','current_in_game_bonus', \
                             'current_finalround_bonus', 'total_payment']
    outcome_config = {key:config[key] for key in outcome_config_params}

    # not needed?
    answerer_type = config['answerer_type']
    translator_type = config['translator_type']

    debug_show_answer = True
    debug_logging = True

    ######################################################################################
    # load
    image_pool_json = json.load(open(image_pool_json_filename,'r'))
    all_images_filenames = json.load(open(all_images_filenames_filename,'r'))
    categories = json.load(open(categories_json_filename,'r'))


    image_pool = image_pool_json[pool_index]

    pool_image_ids_and_target = random.sample(image_pool['pools'][difficulty_level], num_ims_in_pool)
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

    task_data = {
        "post_endpoint": post_endpoint,
        "get_endpoint": get_endpoint,
        "bot_intro_message": intro_message,
        "img_list": img_list,
        "target_image": target_image_url,
        "target_image_id": target_image_id,
        "img_id_list": json.dumps(image_list),
        "max_rounds": max_rounds,
        "num_of_games_in_a_hit": 1,
        "disabled": False,
        "total_bonus_so_far": 0,
        "starting_final_bonus": starting_final_bonus,
        "bonus_deduction_on_each_click": bonus_deduction_on_each_click,
        "base_payment": base_payment,
        "next_game_id": 1,
        "bonus_for_correct_image_after_each_round": bonus_for_correct_image_after_each_round,
        "show_feedback_modal": False,
        "static_data_dir": static_data_dir,
        "translator_type": translator_type,
        "answerer_type": answerer_type,
        "pool_index": pool_index,
        "difficulty_level": difficulty_level,
        "study_type": "",
        "study_description": "",
        "debug_show_answer": debug_show_answer,
        "debug_logging": debug_logging,
        "url_prefix": url_prefix,
        "completed_hit_output": json.dumps(outcome_config)
    }

    return task_data



    


def fetch_completed_hits(hit_ids, approve=True, sandbox=False):
    """Grabs the results for the hit ids.

    Args:
        hit_ids: A list of hit ids to fetch.
        approve: Whether to approve the hits that have been submitted.
        sandbox: Whether to interact on sandbox or production.

    Returns:
        A dictionary from hit_id to the result, if that hit_id has
        been submitted.
    """
    #import pdb;pdb.set_trace()
    et = EasyTurk(sandbox=sandbox)
    output = {}
    for hit_id in hit_ids:
        results = et.get_results(hit_id, reject_on_fail=False)
        if len(results) > 0:
            output[hit_id] = results
            if approve:
                for assignment in results:
                    assignment_id = assignment['assignment_id']
                    et.approve_assignment(assignment_id)
    return output
