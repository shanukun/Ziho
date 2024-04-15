![build](https://img.shields.io/github/actions/workflow/status/shanukun/Ziho/ziho.yml)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/shanukun/Ziho/main)

# Ziho

Ziho is an online programme for flashcards. It helps the user memorise information by utilising cognitive science strategies like spaced repetition and active recall testing.


## Built With

- [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- [SQLite](https://sqlite.org/)
- [Docker](https://www.docker.com/)

## Screenshots

<p float="left">
<img src="./screenshots/home.png" width="400">
<img src="./screenshots/create-deck.png" width="400">
<img src="./screenshots/view-deck.png" width="400">
<img src="./screenshots/study.png" width="400">
<img src="./screenshots/updatecard.png" width="400">
<img src="./screenshots/profile.png" width="400">
<img src="./screenshots/explore.png" width="400">
</p>


## Getting Started 

### Install & Run

- Setup
```
./tools/setup
```

- Run

```
./tools/run-ziho
```

- For dev enviroment 

```
./tools/run-ziho-dev
```

- For docker container

```
docker compose up
```

## Contribution

**Be consistent with existing code**

### Use the linters

```
./tools/lint_and_format
```

### Use the tests

```
pytest tests/
```
