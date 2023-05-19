# Library Report

![Tests](https://img.shields.io/github/actions/workflow/status/ovimatei/library-report/ci.yml?branch=main)


[![Coverage](https://img.shields.io/badge/coverage-72%25-brightgreen)](coverage_report_url)


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