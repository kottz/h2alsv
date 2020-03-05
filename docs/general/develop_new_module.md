# Developing a new module

Please read this page if you are a new developer joining this project. It
outlines some basic principles relevant to h2alsv. 

## General Practices

If possible, new python modules should be `asyncio` based with `async/await`
syntax. All modules use separate configuration files written in TOML. 

Follow the h2alsv JSON [specification](general/h2alsv_protocol.md) for sending
sensor data and logs.

## Dependencies

This project requires Python 3.6+ and Node.js. It is highly advised to use pip
to manage Python dependencies.
Required Python modules can be found in the `requirements.txt` file in the
project root. You are also encouraged to create a virtual python environment.
Please read the [Virtualenv](https://virtualenv.pypa.io/en/latest/) documentation
for instructions.

Node is required for the Web app which is written in React. npm is needed to
run the app.
## Git Workflow

The `develop` branch should be considered the main branch. `master` will only
be used for tested releases. When implementing a new feature make a new local
feature branch off of `develop`. When the feature is completed please rebase or
merge the changes onto the `develop` branch. Then push your changes to GitHub.
Please do not push to `master`. Do not merge `develop`onto `master` unless the
current develop commit has been thouroughly tested and documented.

All documentation should preferably be commited together with the featured code. 
No code will be accepted without proper documentation.

## Writing Documentation
The project documentation can be found in the `docs/` folder. Everything is
written in Markdown. [Docsify](https://docsify.js.org/#/) is used to generate
a static site from the `.md` files.

To add a new page to the documentation simply create a new `.md` file and update
the `_sidebar.md` file with a link to the created file. When pushed to GitHub
the page will automatically be rebuilt. It should be noted that https://h2alsv.se/
tracks the `docs` folder of the `master` branch. The website will not be updated
when new changes are added to the `develop` branch.

[`docsify-cli`](https://github.com/docsifyjs/docsify-cli) allows you to build
your documentation locally before committing it to git. `docsify-cli` is
available through npm. Install it globally with

```bash
npm i docsify-cli -g
```
To serve your documentation locally run the following command from the project
root.
```bash
docsify serve docs
```
Your documentation can now be accessed at `localhost:3000`. If you run into 
problems with installing or building the docs please refer to the `docsify-cli`
[documentation](https://github.com/docsifyjs/docsify-cli).
