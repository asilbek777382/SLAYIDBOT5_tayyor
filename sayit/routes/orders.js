const express = require('express');
const { body, validationResult } = require('express-validator');
const Order = require('../models/Order');
const User = require('../models/User');
const { authorize } = require('../middleware/auth');
const router = express.Router();

// Service prices (so'm)
const SERVICE_PRICES = {
  plumber: 150000,
  electrician: 200000,
  cleaner: 100000,
  carpenter: 300000,
  painter: 250000,
  mechanic: 400000
};

// Create order
router.post('/', [
  authorize('client'),
  body('service').isIn(Object.keys(SERVICE_PRICES)).withMessage('Noto\'g\'ri xizmat turi'),
  body('description').isLength({ min: 10, max: 500 }).withMessage('Tavsif 10-500 belgi orasida bo\'lishi kerak'),
  body('address').notEmpty().withMessage('Manzil talab qilinadi'),
  body('scheduledDate').isISO8601().withMessage('Noto\'g\'ri sana formati')
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

    const { service, description, address, scheduledDate, notes } = req.body;
    
    const scheduledDateTime = new Date(scheduledDate);
    if (scheduledDateTime <= new Date()) {
      return res.status(400).json({
        success: false,
        message: 'Rejalashtirilgan sana kelajakda bo\'lishi kerak'
      });
    }

    const price = SERVICE_PRICES[service];

    const order = new Order({
      client: req.user._id,
      service,
      description,
      address,
      scheduledDate: scheduledDateTime,
      price,
      notes
    });

    await order.save();
    await order.populate('client', '-password');

    // Find available workers for this service
    const availableWorkers = await User.find({
      role: 'ishchi',
      specialization: service,
      isActive: true
    });

    // Send real-time notification to workers
    const io = req.app.get('socketio');
    const connectedUsers = req.app.get('connectedUsers');

    availableWorkers.forEach(worker => {
      const socketId = connectedUsers.get(worker._id.toString());
      if (socketId) {
        io.to(socketId).emit('new_order', {
          orderId: order._id,
          service: order.service,
          description: order.description,
          address: order.address,
          scheduledDate: order.scheduledDate,
          price: order.price,
          client: {
            username: order.client.username,
            phone: order.client.phone
          }
        });
      }
    });

    res.status(201).json({
      success: true,
      message: 'Buyurtma muvaffaqiyatli yaratildi',
      order
    });

  } catch (error) {
    console.error('Create order error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Get orders (with role-based filtering)
router.get('/', async (req, res) => {
  try {
    const { status, page = 1, limit = 10 } = req.query;
    const skip = (page - 1) * limit;

    let query = {};
    
    // Role-based filtering
    if (req.user.role === 'client') {
      query.client = req.user._id;
    } else if (req.user.role === 'ishchi') {
      query.service = req.user.specialization;
    }
    // Admin can see all orders (no additional filtering)

    if (status) {
      query.status = status;
    }

    const orders = await Order.find(query)
      .populate('client', '-password')
      .populate('worker', '-password')
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await Order.countDocuments(query);

    res.json({
      success: true,
      orders,
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(total / limit),
        totalOrders: total,
        hasMore: skip + orders.length < total
      }
    });

  } catch (error) {
    console.error('Get orders error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Get single order
router.get('/:id', async (req, res) => {
  try {
    const order = await Order.findById(req.params.id)
      .populate('client', '-password')
      .populate('worker', '-password');

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Buyurtma topilmadi'
      });
    }

    // Check permissions
    if (req.user.role === 'client' && !order.client._id.equals(req.user._id)) {
      return res.status(403).json({
        success: false,
        message: 'Ruxsat berilmagan'
      });
    }

    if (req.user.role === 'ishchi' && order.service !== req.user.specialization) {
      return res.status(403).json({
        success: false,
        message: 'Ruxsat berilmagan'
      });
    }

    res.json({
      success: true,
      order
    });

  } catch (error) {
    console.error('Get order error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Assign worker to order
router.patch('/:id/assign', authorize('ishchi'), async (req, res) => {
  try {
    const order = await Order.findById(req.params.id);

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Buyurtma topilmadi'
      });
    }

    if (order.service !== req.user.specialization) {
      return res.status(403).json({
        success: false,
        message: 'Bu xizmat turi sizning mutaxassisligingizga mos kelmaydi'
      });
    }

    if (order.status !== 'pending') {
      return res.status(400).json({
        success: false,
        message: 'Bu buyurtma allaqachon tayinlangan yoki yakunlangan'
      });
    }

    order.worker = req.user._id;
    order.status = 'assigned';
    await order.save();

    await order.populate('client', '-password');
    await order.populate('worker', '-password');

    // Notify client
    const io = req.app.get('socketio');
    const connectedUsers = req.app.get('connectedUsers');
    const clientSocketId = connectedUsers.get(order.client._id.toString());

    if (clientSocketId) {
      io.to(clientSocketId).emit('order_assigned', {
        orderId: order._id,
        worker: {
          username: order.worker.username,
          phone: order.worker.phone,
          specialization: order.worker.specialization
        },
        message: 'Sizning buyurtmangizga ishchi tayinlandi'
      });
    }

    res.json({
      success: true,
      message: 'Buyurtma muvaffaqiyatli qabul qilindi',
      order
    });

  } catch (error) {
    console.error('Assign order error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Update order status
router.patch('/:id/status', async (req, res) => {
  try {
    const { status } = req.body;
    const validStatuses = ['in_progress', 'completed', 'canceled'];

    if (!validStatuses.includes(status)) {
      return res.status(400).json({
        success: false,
        message: 'Noto\'g\'ri status'
      });
    }

    const order = await Order.findById(req.params.id)
      .populate('client', '-password')
      .populate('worker', '-password');

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Buyurtma topilmadi'
      });
    }

    // Check permissions
    if (req.user.role === 'ishchi' && !order.worker?._id.equals(req.user._id)) {
      return res.status(403).json({
        success: false,
        message: 'Ruxsat berilmagan'
      });
    }

    if (req.user.role === 'client' && !order.client._id.equals(req.user._id)) {
      return res.status(403).json({
        success: false,
        message: 'Ruxsat berilmagan'
      });
    }

    order.status = status;
    await order.save();

    // Send notification to relevant parties
    const io = req.app.get('socketio');
    const connectedUsers = req.app.get('connectedUsers');

    const targetUserId = req.user.role === 'ishchi' 
      ? order.client._id.toString()
      : order.worker?._id.toString();

    if (targetUserId) {
      const socketId = connectedUsers.get(targetUserId);
      if (socketId) {
        io.to(socketId).emit('order_status_updated', {
          orderId: order._id,
          status: order.status,
          message: `Buyurtma holati yangilandi: ${status}`
        });
      }
    }

    res.json({
      success: true,
      message: 'Buyurtma holati yangilandi',
      order
    });

  } catch (error) {
    console.error('Update order status error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

module.exports = router;