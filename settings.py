from os import environ

# Need to make a draft experiment structure, then can go from there (at least for initial bits).
# Next, need to go through HTML and make sure minute details are patched up
#    Demographic survey

SESSION_CONFIGS = [
    dict(
        name='Introduction',
        display_name='Introduction',
        num_demo_participants=1,
        app_sequence=['Introduction']
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
        display_name='Task_WTP2',
        num_demo_participants=1,
        app_sequence=['Task_WTP'],
        continuation_rv=0.01,
        tried_fancy_pizza=False,
        tried_cheap_pizza=False,
        tried_fancy_taco=False,
        tried_cheap_taco=False
    ),
    dict(
        name='Choice',
        display_name='Choice',
        num_demo_participants=1,
        app_sequence=['Choice'],
        pair1=["Fancy Pizza", "Cheap Taco"],
        pair2=["Fancy Taco", "Cheap Pizza"],
    )

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['treatment', 'start_time', 'end_time', 'time_before_tasks', 'time_taken',
                      'tried_fancy_pizza', 'tried_cheap_pizza', 'tried_fancy_taco', 'tried_cheap_taco', 'tried_ge_3',
                      # Tried before variables
                      'BDM_Score', 'Q1_Correct', 'Q2_Correct', 'Q3_Correct', 'Q4_Correct', 'Q5_Correct',  # BDM
                      'Fancy_Pizza_Value', 'Cheap_Pizza_Value', 'Fancy_Taco_Value',  # Task_WTP
                      'Cheap_Taco_Value',
                      'pair1', 'pair2', 'sub_menu1', 'sub_menu2', 'path', 'rand_task',
                      'treatment_used1', 'treatment_used2', 'blunder_choice1', 'blunder_choice2',  # Choice
                      'treatment_choice1', 'treatment_choice2', 'control_choice1', 'control_choice2',
                      'switched1', 'switched2',
                      'menu_choice1', 'menu_choice2',  # Menu_Select
                      'lc1a', 'pair', 'stage', 'task_to_complete', 'opt_choice1', 'opt_choice2',  # Dynamic Vars
                      'uniID']  # ID Vars
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '5795236920217'
