import os
from setuptools import setup, find_packages

install_requires = [
    ('psycopg2-binary', '2.9.5'),
    ('alembic', '1.8.1'),
    ('environs', '9.5.0'),
    ('psutil', '5.9.4'),
    ('requests', '2.26.0'),
    ('numpy', '1.21.2'),
    ('fastapi', '0.85.0'),
    ('pydantic', '1.9.2'),
    ('SQLAlchemy', '2.0.6'),
    ('prometheus-client', '0.15.0'),
    ('psutil', '5.9.4'),
    ('uvicorn[standard]', '0.17.6'),
    ('loguru', '0.6.0'),
    ('pendulum', '2.1.2'),
    ('pytest', '7.3.0'),
    ('flake8', '6.0.0'),
    ('asyncpg', '0.25.0'),
    ('greenlet', '2.0.2'),
    ('passlib', '1.7.4'),
    ('mailjet-rest', '1.3.4'),
    ('email-validator', '2.0.0.post1'),
    ('bcrypt', '4.0.1'),
    ('pyjwt[crypto]', '2.6.0'),
    ('asyncstdlib', '3.10.7'),
    ('fastapi-pagination[sqlalchemy]', '0.12.0'),
    ('pytz', '2023.3'),
    ('aiohttp', '3.8.4'),
    ('boto3', '1.28.8'),
    ('python-multipart', '0.0.6'),
    ('APScheduler', '3.10.1')
]

CI_PROJECT_NAME = os.environ.get("CI_PROJECT_NAME", "makers")
ARTIFACT_VERSION = os.environ.get("ARTIFACT_VERSION", "0.2.6")
CI_PROJECT_TITLE = os.environ.get("CI_PROJECT_TITLE", "Backend service")
CI_PROJECT_URL = os.environ.get("CI_PROJECT_URL", "https://github.com/makersdevs/teamwork_backend")


setup(
    name=CI_PROJECT_NAME,
    version=ARTIFACT_VERSION,
    description=CI_PROJECT_TITLE,
    url=CI_PROJECT_URL,
    install_requires=["==".join(req) for req in install_requires],
    python_requires=">=3.10.3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            CI_PROJECT_NAME + " = " + "makers.main:execute",
        ]
    },
    include_package_data=True,
    package_data={
        "makers": ["*.ini"],
        "makers.migrations": ["script.py.mako"]
    },
)