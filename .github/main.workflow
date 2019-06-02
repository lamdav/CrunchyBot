workflow "Test" {
  on = "push"
  resolves = ["Test Action"]
}

action "Test Action" {
  uses = "./actions/test"
}
