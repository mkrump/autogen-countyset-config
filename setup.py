from setuptools import setup

setup(
    name='autogen_configs',
    version='',
    packages=['autogen_configs'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'generate_configs = autogen_configs.generation:main',
        ],
    },
    install_requires=['jinja2'],
    tests_require=['pytest'],
)
