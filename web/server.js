// Deliberately vulnerable Express app for GH-500 practice. DO NOT DEPLOY.
// Gives CodeQL a second language so you can practise matrix builds and categories.
const express = require("express");
const { exec } = require("child_process");
const fs = require("fs");
const path = require("path");
const _ = require("lodash");

const app = express();
app.use(express.json());

// CWE-78: Command injection -> js/command-line-injection
app.get("/lookup", (req, res) => {
  exec("nslookup " + req.query.domain, (err, stdout) => res.send(stdout));
});

// CWE-22: Path traversal -> js/path-injection
app.get("/file", (req, res) => {
  res.send(fs.readFileSync(path.join(__dirname, "public", req.query.name)));
});

// CWE-79: Reflected XSS -> js/reflected-xss
app.get("/greet", (req, res) => {
  res.send("<p>Hi " + req.query.name + "</p>");
});

// CWE-94: Code injection -> js/code-injection
app.post("/calc", (req, res) => {
  res.send(String(eval(req.body.expression)));
});

// CWE-1321: Prototype pollution via vulnerable lodash version (Dependabot) and merge
app.post("/settings", (req, res) => {
  const settings = {};
  _.merge(settings, req.body);
  res.json(settings);
});

app.listen(3000);
