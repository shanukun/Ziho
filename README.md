<p align="center">
    <img title="Ziho Logo" src="https://shanukun.github.io/static/images/ziho/ziho-logo.png" align="center">
</p>

<p align="center">
  <b>Create, Study and Share</b> decks of flashcards.
  <br>
   <b>
    <a href="http://ziho.pythonanywhere.com">Demo</a>
  </b>
</p>

<p align="center">

  <a href="https://img.shields.io/github/actions/workflow/status/shanukun/Ziho/ziho.yml">
    <img title="Build Status" src="https://img.shields.io/github/actions/workflow/status/shanukun/Ziho/ziho.yml" />
  </a>
  <a href="https://img.shields.io/github/commit-activity/w/shanukun/Ziho/main">
    <img title="Github commit activity" src="https://img.shields.io/github/commit-activity/w/shanukun/Ziho/main" />
  </a>
</p>


## About

Ziho is a provides a better online interface for Anki than [Anki Web](https://ankiweb.net/decks).
Ziho allows you to create, study and easily share and clone decks, as well as edit them online. 

The backend is built with **Flask**, and the [fsrs](https://github.com/open-spaced-repetition) algorithm is used for spaced repetition.
Following were also used:
- Bootstrap
- SQLAlchemy
- Docker


<span><img src="https://shanukun.github.io/static/images/ziho/home.png"  width="40%"></span>
<span><img src="https://shanukun.github.io/static/images/ziho/study-deck.png" width="35%"></span>

You can find more screenshots [here](https://shanukun.github.io/ziho-ss/).


## Getting Started 

### Quick Start with Docker

> [!Note]  
> Please ensure you have Docker and Docker Compose installed on your system.

1. **Clone the Repository.**
2. **Start the Docker Container:**
    ```bash
    docker compose up -d
    ```

### Local Setup

> [!IMPORTANT]  
> Please ensure you have pip installed on your system.

1. **Clone the Repository.**
2. **Run the setup script:**
    ```bash
    ./tools/setup
    ```
3. **Set up your environment variables in a `.env` file: To run without debug mode, set `DEBUG_MODE=off`.** 
    - Set following for using MySQL
        - MYSQL_USER
        - MYSQL_PASS
        - MYSQL_HOST
        - MYSQL_PORT
        - MYSQL_DB
4. **Start the webapp:**
    ```bash
    ./tools/run-ziho
    ```

## Contributing

1. Follow the code style. Run the following to test the format.
    ```bash
    ./tools/test_lint
    ```
2. Format the code using:
    ```bash
    ./tools/lint_and_format
    ```
3. Make sure to add the tests for new routes
    ```bash
    pytest ./tests
    ```

 
