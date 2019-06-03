workflow "test and publish on tag" {
  on = "push"
  resolves = ["pypi"]
}

workflow "run" {
  on = "schedule(0 0 1 * *)"
  resolves = ["execute"]
}

action "black" {
  uses = "./actions/black"
}

action "pytest" {
  uses = "./actions/pytest"
}

action "tag-filter" {
  needs = [
    "pytest",
    "black"
  ]
  uses = "actions/bin/filter@master"
  args = "tag"
}

action "pypi" {
  needs = "tag-filter"
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
