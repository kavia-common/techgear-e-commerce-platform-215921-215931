#!/bin/bash
cd /home/kavia/workspace/code-generation/techgear-e-commerce-platform-215921-215931/ecommerce_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

