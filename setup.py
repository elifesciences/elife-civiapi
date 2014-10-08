from setuptools import setup, find_packages

setup(
    name='elife-civiapi',
    version='1.0.1',
    install_requires=[
        "requests",
        "html2text",
    ],
    packages=find_packages(exclude=['docs', 'tests*']),
    url='https://github.com/elifesciences/elife-civiapi',
    license='',
    author='Ruth Ivimey-Cook',
    author_email='r.ivimeycook@elifesciences.org',
    description='Python script to read text of a CiviCRM mail template and create it on a Civi server.',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points="""\
[console_scripts]
mailcivi = mailcivi:mailcivi"""
)
