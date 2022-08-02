import logging
import logging.config


def configure_log(test_name):
    dict_config = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': f'../logs/{test_name}.log',
                'mode': 'w',
            },
            'console': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default', 'console'],
                'level': 'INFO',
                'propagate': False
            },
            '__main__': {  # if __name__ == '__main__'
                'handlers': ['default'],
                'level': 'INFO',
                'propagate': False
            },
        }
    }
    logging.config.dictConfig(dict_config)
