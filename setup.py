import re
from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("src/cheetah/__init__.py", "r", encoding="utf8") as f:
    content = f.read()
    author = re.search(r'__author__ = "(.*?)"', content).group(1)
    version = re.search(r'__version__ = "(.*?)"', content).group(1)
    author_email = re.search(r'__contact__ = "(.*?)"', content).group(1)

setup(
    name="cheetah",
    version=version,
    author=author,
    author_email=author_email,
    description="十方教育跑团积分统计工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alphajc/cheetah",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3",
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    entry_points={
        "console_scripts": [
            "cheetah = cheetah.cli:daemon",
            "cheetahctl = cheetah.cli:cli",
        ]
    }
)

