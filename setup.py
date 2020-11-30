import setuptools
from pathlib import Path


setuptools.setup(
    name="search_engines",
    version="1.0.1",
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
    install_requires=[
        'lxml',
    ]
)
