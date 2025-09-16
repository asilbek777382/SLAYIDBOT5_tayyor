const mongoose = require('mongoose');

const orderSchema = new mongoose.Schema({
  client: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  worker: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  },
  service: {
    type: String,
    required: true,
    enum: ['plumber', 'electrician', 'cleaner', 'carpenter', 'painter', 'mechanic']
  },
  description: {
    type: String,
    required: true,
    maxlength: 500
  },
  address: {
    type: String,
    required: true
  },
  scheduledDate: {
    type: Date,
    required: true
  },
  price: {
    type: Number,
    required: true,
    min: 0
  },
  status: {
    type: String,
    enum: ['pending', 'assigned', 'paid', 'in_progress', 'completed', 'canceled'],
    default: 'pending'
  },
  paymentId: {
    type: String
  },
  notes: {
    type: String,
    maxlength: 1000
  }
}, {
  timestamps: true
});

// Index for efficient queries
orderSchema.index({ client: 1, status: 1 });
orderSchema.index({ worker: 1, status: 1 });
orderSchema.index({ service: 1, status: 1 });

module.exports = mongoose.model('Order', orderSchema);