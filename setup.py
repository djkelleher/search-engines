import setuptools
from pathlib import Path

def get_requirements():
    with Path(__file__).parent.joinpath("requirements.txt").open(mode='r') as infile:
        return [r.strip() for r in infile]

setuptools.setup(
    name="search_engines",
    version="1.0.0",
    author="Dan Kelleher",
    author_email="danielkelleher@protonmail.com",
    maintainer='Dan Kelleher',
    maintainer_email='danielkelleher@protonmail.com',
    description="Query and scrape search engines.",
    packages=["search_engines"],
    url="https://github.com/djkelleher/search_engines",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=get_requirements()
)
