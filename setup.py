from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    readme = f.read()

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name='sentiment',
    version='1.0',
    packages=find_packages(exclude=('tests',)),
    package_data={'sentiment': ['data/*/*']},
    description='Inference Sentiment',
    long_description=readme,
    install_requires=requirements,
    include_package_data=True,
    license="MIT",
    author='Lifeweb',
    author_email='info@lifeweb.ir',
    url='https://lifeweb.ir',
    maintainer='AI',
    platforms='all'
)
