# setup.py
from setuptools import setup, find_packages

setup(
    name="task_tracker",                   # любое одно-сложное имя
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        # prod-зависимости скопируйте из requirements.txt
        # или оставьте пустым — CI уже поставит их через pip install -r
    ],
)
# setup.py
from setuptools import setup, find_packages

setup(
    name="task_tracker",                   # любое одно-сложное имя
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        # prod-зависимости скопируйте из requirements.txt
        # или оставьте пустым — CI уже поставит их через pip install -r
    ],
)
