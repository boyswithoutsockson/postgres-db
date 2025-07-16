# Eduri

A platform for exploring and visualizing data from the [Finnish Parliament](https://www.eduskunta.fi/EN/Pages/default.aspx).

## Setup

The sanctioned development workflow requires using a [Dev container](https://code.visualstudio.com/docs/devcontainers/containers) for running the project and its dependencies. This makes it simple to run the required PostgreSQL database and to version any needed OS-level tools.

When managing the project, all required scripts can be found in `Makefile`. Running `make` also lists the relevant ones in your terminal.

After cloning this repository, run `make database` to download all the raw data, preprocess it from the raw Eduskunta API form into the shape of our database, and then finally insert it into the DB. When developing the data pipelines, you likely need to run `make nuke` to clear it before recreating it with the new scripts. For a shorthand, you can also do `make nuke database` for both.

For the web UI, you can spin it up with `make frontend`, which starts a development server running on `localhost:4321`
