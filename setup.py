from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
requirements = requirements.strip().split('\n')

setup(
    name = 'src',
    packages=find_packages(),
    version = '0.0.1',
    author = 'Flavia',
    author_email = 'flavithalopes@hotmail.com',
    description = 'KDD',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/FlaviaLopes/spatio-temporal-analysis-calazar',
    project_urls = {
        "Bug Tracker": "https://github.com/FlaviaLopes/spatio-temporal-analysis-calazar/issues"
    },
    license = 'MIT',
    install_requires = requirements,
)

