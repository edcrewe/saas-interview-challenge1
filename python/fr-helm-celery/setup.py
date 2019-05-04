import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "0.0.1"

with open("README.rst", "r") as fp:
    description = fp.read() + "\n"
for fname in ("USAGE.rst", "HISTORY.rst"):
    with open(fname, "r") as fp:
        description += fp.read() + "\n"

setup(
    name="fr-helm-celery",
    author="Ed Crewe",
    author_email="edmundcrewe@gmail.com",
    url="https://github.com/ForgeCloud/saas-interview-challenge1",
    description="Creates a RESTful microservice for scheduling Helm tasks to deploy ForgeRock components",
    license="Apache",
    version=version,
    long_description=description,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: ForgeRock",
        "Natural Language :: English",
        "Development Status :: 1 - Alpha",
        "Framework :: Celery",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
    ],
    include_package_data=True,
    packages=["fr_helm_celery"],
    zip_safe=False,
    install_requires=["pyhelm", "celery"],
    entry_points="""
      # -*- Entry points: -*-
      """,
)
