from setuptools import setup, find_packages

setup(
    name="mlog-developer-test",  # Package name
    version="0.0.2",            # Initial version
    author="Masoud Heidary",
    author_email="Masoud.Hei.dev@gmail.com",
    description="A simple log library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/...",  # Replace with your GitHub URL
    packages=find_packages(),   # Automatically find packages in the directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",    # Minimum Python version
    install_requires=[],        # Dependencies (add them if needed, e.g., `["requests"]`)
)