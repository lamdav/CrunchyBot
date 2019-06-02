workflow "test" {
  on = "push"
  resolves = ["pytest"]
}

action "black" {
  uses = "./actions/black"
}

action "pytest" {
  needs = "black"
  uses = "./actions/pytest"
}
