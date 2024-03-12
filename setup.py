import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name='slackwebhook',
  version='1.3.0',
  author='Ben Sokol',
  author_email='ben@bensokol.com',
  maintainer='Ben Sokol',
  maintainer_email='ben@bensokol.com',
  description='Send messages to a slack webhook',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://git.bensokol.com/slackwebhook',
  download_url='https://git.bensokol.com/slackwebhook',
  project_urls={
    "Bug Tracker": "https://git.bensokol.com/slackwebhook/issues"
  },
  entry_points={
    'console_scripts': [
      'slackwebhook = slackwebhook.slackwebhook:main',
    ],
  },
  license='MIT',
  packages=['slackwebhook'],
)
