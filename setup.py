from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='quantumlounge',
      version=version,
      description="Project Management for humans",
      long_description="""\
A status stream inspired project management tool""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='pm projectmanagement status activitystreams streams projects communication web',
      author='Christian Scholz',
      author_email='cs@comlounge.net',
      url='http://quantumlounge.org',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'werkzeug',
          'simplejson',
          'routes',
          'logbook',
          'py',
          'python-dateutil',
          'formencode',
          'quantumcore.storages',
          'quantumcore.exceptions',
          'quantumcore.resources'
      ],
      entry_points={
        'paste.app_factory': [
            'main=quantumlounge.http.main:app_factory',
            ],
        }
      )
