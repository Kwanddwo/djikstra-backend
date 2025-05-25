# Heroku CLI

You need Heroku's CLI to run this app locally with Heroku Inference and Agents, then put the Inference Id Heroku gives you in your .env file

To run locally: `heroku local dev`

If this Throws an error complaining about **parsing Unicode characters**, then add the following line to your env file: 
`export PYTHONIOENCODING=utf-8`

# Whenever you import something new

Don't forget to put it in requirements.txt! That's important for deployment.
Virtual environments will need that file to install dependencies, which is way better than using global libraries

# Alembic revisions

To update the database schema, run the following:
`alembic --autogenerate -m "Revision Message"`
and then to upgrade to the revision, run:
`alembic upgrade head`
(This should be done locally as well as on heroku, if you want to open a bash session on the remote server, run: `heroku run bash`)
