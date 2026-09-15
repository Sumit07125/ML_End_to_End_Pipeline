from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DOT = "-e ."


def get_requirements(file_path: str) -> List[str]:
    """Return install requirements from a pip requirements file."""
    requirements = []

    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "").strip() for req in requirements]
        requirements = [
            req for req in requirements if req and not req.startswith("#")
        ]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

        return requirements


setup(
    name="ML_End_to_End_Pipeline",
    author="Sumit Mali",
    version="0.0.1",
    author_email="sumitmali07125@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)
