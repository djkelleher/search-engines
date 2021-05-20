import setuptools
from pathlib import Path


setuptools.setup(
    name="search_engines",
    version="1.0.7",
    author="Dan Kelleher",
    author_email="kelleherjdan@gmail.com",
    maintainer='Dan Kelleher',
    maintainer_email='kelleherjdan@gmail.com',
    description="Query and scrape search engines.",
    packages=["search_engines"],
    url="https://github.com/djkelleher/search_engines",
    long_description=Path(__file__).parent.joinpath('README.md').read_text(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['lxml'],
    extras_require={
        'test': ['pyppeteer'],
    },
)
