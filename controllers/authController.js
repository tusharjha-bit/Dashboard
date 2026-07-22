exports.loginUser = (req, res) => {
  const { email, password } = req.body;

  if (email === "admin@gmail.com" && password === "1234") {
    res.json({ success: true });
  } else {
    res.status(401).json({ success: false });
  }
};