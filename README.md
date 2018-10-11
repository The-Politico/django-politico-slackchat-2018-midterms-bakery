![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-politico-slackchat-2018-midterms-bakery

### Quickstart

1. Install the app.

  ```
  $ pip install django-politico-slackchat-2018-midterms-bakery
  ```

2. Add the app to your Django project and configure settings.

  ```python
  INSTALLED_APPS = [
      # ...
      'slackchatbakery',
  ]

  #########################
  # slackchatbakery settings

  SLACKCHATBAKERY_SECRET_KEY = ""
  SLACKCHATBAKERY_SLACKCHAT_CHANNEL_ENDPOINT = "" # Endpoint for serializer API
  SLACKCHATBAKERY_WEBHOOK_VERIFICATION_TOKEN = "" # Verification token from serializer
  SLACKCHATBAKERY_AWS_ACCESS_KEY_ID = ""
  SLACKCHATBAKERY_AWS_SECRET_ACCESS_KEY = ""
  SLACKCHATBAKERY_AWS_S3_BUCKET = ""
  SLACKCHATBAKERY_AWS_REGION = "" # e.g. us-east-2
  SLACKCHATBAKERY_CLOUDFRONT_ALTERNATE_DOMAIN = ""
  SLACKCHATBAKERY_S3_UPLOAD_ROOT = "" # e.g. election-results/2018/live-analysis/midterms/
  SLACKCHATBAKERY_S3_STATIC_ROOT = "" #e.g. https://www.politico.com

  ```

### Routes
Given the suggested upload root of `election-results/2018/live-analysis/midterms/`, this app will produce the following routes:

#### Full Chat Data
- Chat: `[STATIC_ROOT]/election-results/2018/live-analysis/midterms/data.json`

#### Body Data
- House: `[STATIC_ROOT]/election-results/2018/live-analysis/midterms/stubs/house/data.json`
- Senate: `[STATIC_ROOT]/election-results/2018/live-analysis/midterms/stubs/senate/data.json`
- Governor: `[STATIC_ROOT]/election-results/2018/live-analysis/midterms/stubs/governor/data.json`

#### State Data
State pages will be created on demand based on the data available. For example, if no races are tagged with a race in Florida, the Florida directory will not exist. If only Florida house races are tagged then a Florida and a Florida House directory will exist, but not a Florida Senate or Florida Governor.
- Whole State: `[STATIC_ROOT]/election-results/2018/live-analysis/midterms/stubs/[STATE_SLUG]/data.json`
  - [https://politico.com/election-results/2018/live-analysis/midterms/stubs/new-mexico/data.json](https://politico.com/election-results/2018/live-analysis/midterms/stubs/florida/data.json)
- State Body: `[STATIC_ROOT]/election-results/2018/live-analysis/midterms/stubs/[STATE_SLUG]/[BODY_SLUG]/data.json`
  - [https://politico.com/election-results/2018/live-analysis/midterms/stubs/florida/senate/data.json](https://politico.com/election-results/2018/live-analysis/midterms/stubs/florida/senate/data.json)

#### Argument Data
This app also comes with special argument-based feeds which create data sets based on the presence of an argument (with some optional filtering). To learn how to make more of these routes see [Making Argument Routes](#making-argument-routes). Those routes include:

##### House Pin
Messages reacted to with the `pushpin` reaction.
-  `[STATIC_ROOT]/election-results/2018/live-analysis/midterms/stubs/house/pinned/data.json`


### Developing

##### Running a development server

Developing python files? Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

Developing static assets? Move into the pluggable app's staticapp directory and start the node development server, which will automatically proxy Django's development server.

  ```
  $ cd slackchatbakery/staticapp
  $ gulp
  ```

Want to not worry about it? Use the shortcut make command.

  ```
  $ make dev
  ```

##### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/slackchatbakery"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```

##### Making Argument Routes
The app comes preloaded with a base class that makes creating new argument-based datasets easy. Start by making a new view file in the [`slackchatbakery/views/arguments`](slackchatbakery/views/arguments) directory.

Paste the following:
```python
from .base import BaseArgument


class ArgumentViewName(BaseArgument):
    name = "slackchatbakery-argument-view-name"
    arg = ""
    path = ""

```

Fill out the view data with the arg that messages in this feed should have as well as the path to which you want to bake data. The path you put here will be directly appended to the `SLACKCHATBAKERY_S3_STATIC_ROOT` + `SLACKCHATBAKERY_S3_UPLOAD_ROOT`. We recommend putting any subsets in the `stubs` directory.

If you create a new route make sure to add it to this README under [Argument Data](#argument-data) with a brief description of what it contains.

###### Where do message args comes from?
Message args will be added in the serializer. See the docs for [reaction-based args](https://django-slackchat-serializer.readthedocs.io/en/latest/serialization.html#args) and [content-based args](https://django-slackchat-serializer.readthedocs.io/en/latest/serialization.html#custom-content-templates) for more on this.

###### Can I filter for more than just the presence of an arg?
Yes! If you want to further filter your data past just "any messages with this arg" you can extend the inherited `filter_messages` method which is called when creating the queryset. This method gets the list of all messages in the channel and should return a list of messages. Let's look at an example that crates a feed of messages with the `test` argument that begin with the letter `T`.

```python
from .base import BaseReaction


class ExampleArg(BaseReaction):
    name = "slackchatbakery-example-arg"
    arg = "test"
    path = "stubs/example/"

    def filter_messages(self, messages):
        return [
            message
            for message in messages
            if message["content"].startswith("T")
        ]
```
*Note that this extra filter step is run BEFORE messages get filtered for the presence of the arg.*

Before you start writing complex filters though make sure to check the `races` utility found in the [`slackchatbakery/utils/races`](slackchatbakery/utils/races) directory. It comes with useful functions like `message_in_body` and `message_in_state` which take a message and some more data as an argument and return a boolean.
