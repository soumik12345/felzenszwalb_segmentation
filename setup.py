from setuptools import setup, find_packages
from pip._internal.req import parse_requirements
from pip._internal.network.session import PipSession


requirements = parse_requirements('requirements.txt', session=PipSession())

setup(
    name="felzenszwalb_segmentation", version="0.1.1",
    description="Implementation of Efficient Graph-Based Image Segmentation",
    long_description="Implementation of Efficient Graph-Based Image Segmentation by Pedro F. Felzenszwalb from Artificial Intelligence Lab, Massachusetts Institute of Technology and Daniel P. Huttenlocher from Computer Science Department, Cornell University.",
    author="Soumik Rakshit", author_email="19soumik.rakshit96@gmail.com", packages=find_packages(),
    install_requires=[str(requirement.requirement) for requirement in requirements]
)
