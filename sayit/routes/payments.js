const express = require('express');
const { body, validationResult } = require('express-validator');
const Order = require('../models/Order');
const Payment = require('../models/Payment');
const { authorize } = require('../middleware/auth');
const router = express.Router();

// Fake payment simulation function
const simulatePayment = async (paymentMethod, amount, cardNumber) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      // 80% success rate for simulation
      const success = Math.random() < 0.8;
      
      if (success) {
        resolve({
          success: true,
          transactionId: 'TXN' + Date.now() + Math.random().toString(36).substr(2, 9),
          status: 'completed'
        });
      } else {
        resolve({
          success: false,
          status: 'failed',
          failureReason: 'Karta balansi yetarli emas'
        });
      }
    }, 2000); // 2 second delay to simulate processing
  });
};

// Process payment
router.post('/:orderId/pay', [
  authorize('client'),
  body('paymentMethod').isIn(['payme', 'click', 'card']).withMessage('Noto\'g\'ri to\'lov usuli'),
  body('cardNumber').matches(/^\d{16}$/).withMessage('Karta raqami 16 ta raqamdan iborat bo\'lishi kerak')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        success: false,
        message: 'Validatsiya xatosi',
        errors: errors.array()
      });
    }

    const { paymentMethod, cardNumber } = req.body;
    const orderId = req.params.orderId;

    // Find order
    const order = await Order.findById(orderId).populate('client', '-password');
    
    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Buyurtma topilmadi'
      });
    }

    // Check if user is the client of this order
    if (!order.client._id.equals(req.user._id)) {
      return res.status(403).json({
        success: false,
        message: 'Ruxsat berilmagan'
      });
    }

    // Check if order can be paid
    if (!['assigned', 'pending'].includes(order.status)) {
      return res.status(400).json({
        success: false,
        message: 'Bu buyurtmani to\'lab bo\'lmaydi'
      });
    }

    // Check if payment already exists
    const existingPayment = await Payment.findOne({ 
      orderId: orderId, 
      status: { $in: ['completed', 'pending'] } 
    });

    if (existingPayment) {
      return res.status(400).json({
        success: false,
        message: 'Bu buyurtma uchun to\'lov allaqachon amalga oshirilgan yoki jarayonda'
      });
    }

    // Create payment record
    const payment = new Payment({
      orderId: order._id,
      amount: order.price,
      paymentMethod,
      cardNumber: cardNumber.slice(-4), // Store only last 4 digits
      status: 'pending'
    });

    await payment.save();

    // Simulate payment processing
    const paymentResult = await simulatePayment(paymentMethod, order.price, cardNumber);

    // Update payment and order based on result
    if (paymentResult.success) {
      payment.status = 'completed';
      payment.transactionId = paymentResult.transactionId;
      await payment.save();

      order.status = 'paid';
      order.paymentId = payment.transactionId;
      await order.save();

      // Send notification to client and worker
      const io = req.app.get('socketio');
      const connectedUsers = req.app.get('connectedUsers');

      // Notify client about payment failure
      const io = req.app.get('socketio');
      const connectedUsers = req.app.get('connectedUsers');
      const clientSocketId = connectedUsers.get(order.client._id.toString());

      if (clientSocketId) {
        io.to(clientSocketId).emit('payment_failed', {
          orderId: order._id,
          reason: paymentResult.failureReason,
          message: 'To\'lov amalga oshmadi'
        });
      }

      res.status(400).json({
        success: false,
        message: 'To\'lov amalga oshmadi',
        reason: paymentResult.failureReason
      });
    }

  } catch (error) {
    console.error('Payment error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Get payment history
router.get('/history', async (req, res) => {
  try {
    const { page = 1, limit = 10 } = req.query;
    const skip = (page - 1) * limit;

    let query = {};
    
    if (req.user.role === 'client') {
      // Get orders for this client
      const clientOrders = await Order.find({ client: req.user._id }).select('_id');
      const orderIds = clientOrders.map(order => order._id);
      query.orderId = { $in: orderIds };
    } else if (req.user.role === 'ishchi') {
      // Get orders assigned to this worker
      const workerOrders = await Order.find({ worker: req.user._id }).select('_id');
      const orderIds = workerOrders.map(order => order._id);
      query.orderId = { $in: orderIds };
    }
    // Admin can see all payments (no additional filtering)

    const payments = await Payment.find(query)
      .populate({
        path: 'orderId',
        populate: {
          path: 'client worker',
          select: '-password'
        }
      })
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Payment.countDocuments(query);

    res.json({
      success: true,
      payments,
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(total / limit),
        totalPayments: total,
        hasMore: skip + payments.length < total
      }
    });

  } catch (error) {
    console.error('Payment history error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Get payment details
router.get('/:paymentId', async (req, res) => {
  try {
    const payment = await Payment.findById(req.params.paymentId)
      .populate({
        path: 'orderId',
        populate: {
          path: 'client worker',
          select: '-password'
        }
      });

    if (!payment) {
      return res.status(404).json({
        success: false,
        message: 'To\'lov ma\'lumotlari topilmadi'
      });
    }

    // Check permissions
    const order = payment.orderId;
    if (req.user.role === 'client' && !order.client._id.equals(req.user._id)) {
      return res.status(403).json({
        success: false,
        message: 'Ruxsat berilmagan'
      });
    }

    if (req.user.role === 'ishchi' && (!order.worker || !order.worker._id.equals(req.user._id))) {
      return res.status(403).json({
        success: false,
        message: 'Ruxsat berilmagan'
      });
    }

    res.json({
      success: true,
      payment
    });

  } catch (error) {
    console.error('Get payment error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

module.exports = router;