from setuptools import setup, find_packages

setup(
    name="croctalk",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[        
        'python-telegram-bot',
        'whisper',
        'requests',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'croctalk = croctalk.main:main',  # Adjust this line if your main function is elsewhere
        ],
    },
)

