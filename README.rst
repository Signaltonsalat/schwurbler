==========
schwurbler
==========

Mangle strings by repeated Google Translate

Description
===========

This module offers functions to destroy text by feeding it through multiple
languages in Google Translate.

Installation
============

The project is available on PyPI, so simply invoke the following to install the
package:

.. code-block::

    pip install schwurbler

Usage
=====

Schwurbler's functions are contained in the ``schwurbler`` package, so simply
import it:

.. code-block:: python

    import schwurbler

The two main functions are fixed path schwurbles and set ratio schwurbles. The
former translates text through a fixed set of languages and the latter randomly
picks languages to translate a string through until it only resembles the
original by a certain token set ratio:

.. code-block:: python

    import schwurbler
    translated = schwurbler.path_schwurbel(['en', 'ja', 'en'], 'Hello world!')
    translates = schwurbler.set_ratio_schwurbel('Hello world!', 'en', ratio=50)

More information on the usage can be found in the `API reference`_.

.. _API reference: https://schwurbler.readthedocs.io/en/latest/
