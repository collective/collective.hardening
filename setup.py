"""Installer for the collective.hardening package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.md").read(),
        open("CONTRIBUTORS.md").read(),
        open("CHANGES.md").read(),
    ]
)


setup(
    name="collective.hardening",
    version="1.0.0a1.dev0",
    description="An addon for hardening Plone",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS Hardening",
    author="ale-rt",
    author_email="alessandro.pisa@gmail.com",
    url="https://github.com/collective/collective.hardening",
    project_urls={
        "PyPI": "https://pypi.org/project/collective.hardening/",
        "Source": "https://github.com/collective/collective.hardening",
        "Tracker": "https://github.com/collective/collective.hardening/issues",
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["collective"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
    install_requires=["setuptools", "Products.CMFPlone"],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.contenttypes[test]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
