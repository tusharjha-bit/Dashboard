exports.makePayment = (req, res) => {
  const { amount } = req.body;

  res.json({
    success: true,
    message: `Payment of ₹${amount} successful`,
  });
};
