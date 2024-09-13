name: Weekly Spotify Data Update

# Controls when the workflow will run
on:
  schedule:
    # Run every Monday at 12:00 AM UTC
    - cron: '0 0 * * MON'

  # Allows the workflow to be triggered manually
  workflow_dispatch:

jobs:
  run_script:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository content
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        pip install requests pandas

    - name: Run Spotify Script
      run: |
        python try.py
