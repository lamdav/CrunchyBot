import os
import pathlib

from setuptools import setup, find_packages

setup_path = pathlib.Path(os.path.dirname(os.path.relpath(__file__)))
with open(setup_path.joinpath("README.md").as_posix(), encoding="utf-8", mode="r") as f:
    long_description = f.read()

setup(
    name="crunchy_bot",
    use_scm_version={"write_to": "./crunchy_bot/client/version.py"},
    setup_requires=["setuptools_scm", "pytest-runner"],
    description="Crunchyroll Guest Pass Publisher for Reddit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="David Lam",
    author_email="david.lam@lamdav.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: MacOS X",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires=[
        "Click==7.0",
        "praw==6.2.0",
        "prawcore==1.0.1",
        "selenium==3.141.0",
    ],
    tests_require=["pytest"],
    python_requires=">=3.5",
    entry_points={"console_scripts": ["crunchy=crunchy_bot.client.cli:cli"]},
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/lamdaV/CrunchyBot/issues",
        "Source": "https://github.com/lamdaV/CrunchyBot",
    },
)
