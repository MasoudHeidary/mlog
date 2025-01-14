from setuptools import setup, find_packages

setup(
    name="mlog",
    version="1.0.0",
    author="Masoud Heidary",
    author_email="Masoud.Hei.dev@gmail.com",
    description="A simple log library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/...",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)