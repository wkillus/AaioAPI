from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r', encoding='UTF-8') as f:
    return f.read()

setup(
  name='AaioAPI',
  version='2.5.5',
  author='Fre4ka',
  author_email='yusufbek0303@gmail.com',
  description='The best, convenient and simple library for connecting Aaio payment',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/wkillus/AaioAPI',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='aaio api python payments aaio-api aaioapi',
  project_urls={
    'Homepage': 'https://github.com/wkillus/AaioAPI',
    'Documentation': 'https://wiki.aaio.io/'
  },
  python_requires='>=3.7'
)