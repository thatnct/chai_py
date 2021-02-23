import setuptools

with open("README.md", "r") as f:
    readme = f.read()

setuptools.setup(
    name="chaipy",
    version="0.1.0",
    author="Nexus",
    author_email="nexus.chai@gmail.com",
    description="A developer interface for creating chatbots for the Chai app.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires='~=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: Apache Software License'
    ]
)