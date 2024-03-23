from setuptools import setup, find_packages

setup(
    name='msqgenerator',
    version='0.0.1',
    author='Naif A. Ganadily',
    author_email='ganadilynaif@gmail.com',
    install_requires=[
        "openai",
        "langchain",
        "streamlit",
        "python-dotenv",
        "PyPDF2"
    ],
    packages=find_packages()
)