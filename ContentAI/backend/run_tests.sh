#!/bin/bash
pytest tests/ -v --cov=app --cov-report=term-missing
