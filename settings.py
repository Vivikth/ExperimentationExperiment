from os import environ

# Need to make a draft experiment structure, then can go from there (at least for initial bits).
# Next, need to go through HTML and make sure minute details are patched up
#    Demographic survey

SESSION_CONFIGS = [
    dict(
        name='Introduction',
        display_name='Introduction',
        num_demo_participants=1,
        app_sequence=['Introduction'],
        next_session="test"
    ),
    dict(
        name='BDM',
        display_name='BDM',
        num_demo_participants=1,
        app_sequence=['BDM']
    ),
    dict(
        name='Task_WTP',
        display_name='Task_WTP',
        num_demo_participants=1,
        app_sequence=['Task_WTP']
    ),
    dict(
        name='Task_WTP2',
        display_name='Task_WTP_never_tried',
        num_demo_participants=1,
        app_sequence=['Task_WTP'],
        continuation_rv=0.01,
        tried_fancy_pizza=1,
        tried_cheap_pizza=2,
        tried_fancy_taco=2,
        tried_cheap_taco=4
    ),
    dict(
        name='Choice',
        display_name='Choice',
        num_demo_participants=1,
        app_sequence=['Choice'],
        pair1=["Fancy Pizza", "Cheap Taco"],
        pair2=["Fancy Taco", "Cheap Pizza"],
    ),
    dict(
        name='Demog_Survey',
        display_name='Survey',
        num_demo_participants=1,
        app_sequence=['Demog_Survey'],
    ),
    dict(
        name='Experiment',
        display_name='Experiment',
        num_demo_participants=1,
        app_sequence=['Introduction', 'BDM', 'Task_WTP', 'Choice', 'bret', 'bigfive', 'Demog_Survey'],
    ),
    dict(
        name='Intro_BOT',
        display_name='Intro_BOT',
        num_demo_participants=1,
        app_sequence=['Introduction'],
        use_browser_bots=True
    ),
    dict(
        name='BDM_BOT',
        display_name='BDM_BOT',
        num_demo_participants=1,
        app_sequence=['BDM'],
        use_browser_bots=True
    ),
    dict(
        name='Task_WTP_BOT',
        display_name='Task_WTP_BOT',
        num_demo_participants=1,
        app_sequence=['Task_WTP'],
        use_browser_bots=True,
        tried_fancy_pizza=1,
        tried_cheap_pizza=1,
        tried_fancy_taco=1,
        tried_cheap_taco=1
    ),
    dict(
        name='Choice_BOT',
        display_name='Choice_BOT',
        num_demo_participants=1,
        app_sequence=['Choice'],
        pair1=["Fancy Pizza", "Cheap Taco"],
        pair2=["Fancy Taco", "Cheap Pizza"],
        BDM_Num=50,
        rand_outcome="No_BDM",
        use_browser_bots=True,
    ),
    dict(
        name='Demog_Survey_BOT',
        display_name='Demog_Survey_BOT',
        num_demo_participants=1,
        app_sequence=['Demog_Survey'],
        use_browser_bots=True,
    ),
    dict(
        name='Experiment_BOT',
        display_name='Experiment_BOT',
        num_demo_participants=1,
        app_sequence=['Introduction', 'BDM', 'Task_WTP', 'Choice', 'Demog_Survey'],
        use_browser_bots=True,
    ),
    dict(
        name='Big_Five',
        display_name='Big Five',
        num_demo_participants=1,
        app_sequence=['bigfive'],
    ),
    dict(
        name='bret',
        display_name='bret',
        num_demo_participants=1,
        app_sequence=['bret'],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc="", next_meal_day="Tuesday", next_meal_time="lunch",
    next_meal_date="18th October", sample_meal_day="Tuesday", sample_meal_time="lunch", sample_meal_date="11th October"
)

PARTICIPANT_FIELDS = ['treatment', 'start_time', 'end_time', 'time_before_tasks', 'time_taken',
                      'tried_fancy_pizza', 'tried_cheap_pizza', 'tried_fancy_taco', 'tried_cheap_taco', 'tried_ge_3',
                      # Tried before variables
                      'BDM_Score', 'Q1_Correct', 'Q2_Correct', 'Q3_Correct', 'Q4_Correct', 'Q5_Correct',  # BDM
                      'Fancy_Pizza_Value', 'Cheap_Pizza_Value', 'Fancy_Taco_Value',  # Task_WTP
                      'Cheap_Taco_Value',
                      'pair1', 'pair2', 'rand_task', 'rand_outcome', 'BDM_Num', 'switch_point',
                      'treatment_used1', 'blunder_choice', 'control_choice',  # Choice
                      'pair', 'stage', 'task_to_complete', 'opt_choice1', 'opt_choice2',  # Dynamic Vars
                      'uniID', 'sample_meal_day', 'sample_meal_date', 'sample_meal_time',
                      'next_meal_day', 'next_meal_date', 'next_meal_time']  # ID Vars


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'AUD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5795236920217'

ROOMS = [
    dict(
        name='econ_lab',
        display_name='Experimental Economics Lab',
    )
]
