const router = require("express").Router();
const { makePayment } = require("../controllers/paymentController");

router.post("/pay", makePayment);

module.exports = router;