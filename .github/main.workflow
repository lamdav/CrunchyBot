workflow "test" {
  on = "push"
  resolves = ["pytest"]
}

workflow "publish" {
  on = "release"
  resolves = ["pypi"]
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
