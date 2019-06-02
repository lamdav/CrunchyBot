workflow "test" {
  on = "push"
  resolves = ["pytest"]
}

workflow "publish" {
  on = "release"
  resolves = ["pypi"]
}

workflow "run" {
  on = "schedule("0 0 1 * *")
  resolves = ["execute"]
}

action "black" {
  uses = "./actions/black"
}

action "pytest" {
  needs = "black"
  uses = "./actions/pytest"
}

action "pypi" {
  needs = "pytest"
  uses = "./actions/pypi"
  secrets = ["TWINE_USERNAME", "TWINE_PASSWORD"]
}

action "execute" {
  uses = "./actions/run"
  secrets = [
    "CRUNCHY_USERNAME",
    "CRUNCHY_PASSWORD",
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USER_AGENT",
    "REDDIT_USERNAME",
    "REDDIT_PASSWORD",
    "LOG_DIR"
  ]
}
