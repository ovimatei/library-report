# Library Report

![Tests](https://github.com/ovimatei/library-report/actions/workflows/tests.yml/badge.svg?branch=main)


[![Coverage](https://img.shields.io/badge/coverage-{{COVERAGE_PERCENTAGE}}%25-brightgreen)](https://github.com/ovimatei/library-report/suites/artifacts/704558135



## Description

This is a program that reads books from Open Library API from given categories
and generates a csv file with the following information:

- Title
- Categories
- Author Names
- Price
- Description

It also uploads the csv file to a Google Sheet.

## Requirements
- Python 3.6+

## Installation
- `pip install -r requirements.txt`

## Usage

- `python main.py`