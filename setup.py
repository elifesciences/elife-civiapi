from distutils.core import setup

setup(
    name='elife-civiapi',
    version='1.0',
    install_requires=[
        "requests",
        "html2text",
        "json",
    ],
    url='https://github.com/elifesciences/elife-civiapi',
    license='',
    author='Ruth Ivimey-Cook',
    author_email='',
    description='Python script to read text of a CiviCRM mail template and create it on a Civi server.'
)
