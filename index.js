const express = require('express');
const app = express();
const port = 3000;

// ❌ false positive — "insecure" hardcoded secret (не используется)
const secret = "123456"; // <-- Semgrep/CodeQL найдут это

// ❌ возможная XSS уязвимость
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.send(`<h1>Results for: ${query}</h1>`); // <-- нет фильтрации
});

// ❌ потенциальный SQL-инъекция (эмуляция)
app.get('/user', (req, res) => {
  const id = req.query.id;
  const query = `SELECT * FROM users WHERE id = ${id}`; // <-- статический анализ поймает
  res.send(`Executing: ${query}`);
});

app.listen(port, () => {
  console.log(`Insecure app listening at http://localhost:${port}`);
});
