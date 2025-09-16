const mongoose = require('mongoose');

const paymentSchema = new mongoose.Schema({
  orderId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Order',
    required: true
  },
  amount: {
    type: Number,
    required: true,
    min: 0
  },
  paymentMethod: {
    type: String,
    enum: ['payme', 'click', 'card'],
    required: true
  },
  status: {
    type: String,
    enum: ['pending', 'completed', 'failed', 'canceled'],
    default: 'pending'
  },
  transactionId: {
    type: String,
    unique: true
  },
  cardNumber: {
    type: String // Last 4 digits only for security
  },
  failureReason: {
    type: String
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Payment', paymentSchema);
