# Jobs folder

Just a place to store jobs. You can use these to test your changes before
uploading to jenkins. After you make a change simply run:

    python jobs.py reconfig --dry

This will render the configs and you can see the changes in git diff.
Please remember to commit these changes with your job changes so we can
see the changes over time.
