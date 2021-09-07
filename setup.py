import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

with open("requirements.txt") as f:
    requireds = f.read().splitlines()

setup(
    name="rembg",
    version="1.0.27",
    description="Remove image background",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danielgatis/rembg",
    author="Daniel Gatis",
    author_email="danielgatis@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="remove, background, u2net",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    install_requires=requireds,
    entry_points={
        "console_scripts": [
            "rembg=rembg.cmd.cli:main",
            "rembg-server=rembg.cmd.server:main",
            "rembg-server-v2=rembg.cmd.server_v2:main",
            "rembg-server-v3=rembg.cmd.server_v3:main",
            "rembg-celery=celery -A src.rembg.cmd.celery_worker.celery worker --loglevel=info --pool=solo",
        ],
    },
)
