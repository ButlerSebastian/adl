from setuptools import setup, find_packages

setup(
    name='adl',
    version='1.5.0',
    description='Agent Definition Language - A vendor-neutral, open standard for defining AI agents',
    author='Next Moca',
    author_email='info@nextmoca.com',
    url='https://github.com/nextmoca/adl',
    license='Apache-2.0',
    packages=find_packages(),
    install_requires=[
        'lark>=1.1.0',
        'pyyaml>=6.0',
    ],
    entry_points={
        'console_scripts': [
            'adl-compile=tools.dsl.cli:cmd_compile',
            'adl-validate=tools.dsl.cli:cmd_validate',
            'adl-format=tools.dsl.cli:cmd_format',
            'adl-lint=tools.dsl.cli:cmd_lint',
            'adl-generate=tools.dsl.cli:cmd_generate',
        ],
    },
    package_data={
        'adl': [
            'schema/*.json',
            'examples/*.adl',
            'docs/*.md',
        ],
    },
    python_requires='>=3.8',
)