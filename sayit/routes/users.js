const express = require('express');
const User = require('../models/User');
const Order = require('../models/Order');
const { authorize } = require('../middleware/auth');
const router = express.Router();

// Get all users (Admin only)
router.get('/', authorize('admin'), async (req, res) => {
  try {
    const { role, page = 1, limit = 20 } = req.query;
    const skip = (page - 1) * limit;

    let query = { isActive: true };
    if (role && ['client', 'ishchi'].includes(role)) {
      query.role = role;
    }

    const users = await User.find(query)
      .select('-password')
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));

    const total = await User.countDocuments(query);

    // Get additional statistics for each user
    const usersWithStats = await Promise.all(users.map(async (user) => {
      const userObj = user.toObject();

      if (user.role === 'client') {
        const orderStats = await Order.aggregate([
          { $match: { client: user._id } },
          {
            $group: {
              _id: null,
              totalOrders: { $sum: 1 },
              totalSpent: { $sum: '$price' },
              completedOrders: {
                $sum: { $cond: [{ $eq: ['$status', 'completed'] }, 1, 0] }
              }
            }
          }
        ]);
        userObj.stats = orderStats[0] || { totalOrders: 0, totalSpent: 0, completedOrders: 0 };
      } else if (user.role === 'ishchi') {
        const workerStats = await Order.aggregate([
          { $match: { worker: user._id } },
          {
            $group: {
              _id: null,
              totalOrders: { $sum: 1 },
              totalEarned: { $sum: '$price' },
              completedOrders: {
                $sum: { $cond: [{ $eq: ['$status', 'completed'] }, 1, 0] }
              }
            }
          }
        ]);
        userObj.stats = workerStats[0] || { totalOrders: 0, totalEarned: 0, completedOrders: 0 };
      }

      return userObj;
    }));

    res.json({
      success: true,
      users: usersWithStats,
      pagination: {
        currentPage: parseInt(page),
        totalPages: Math.ceil(total / limit),
        totalUsers: total,
        hasMore: skip + users.length < total
      }
    });

  } catch (error) {
    console.error('Get users error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Get user profile
router.get('/profile', async (req, res) => {
  try {
    const user = await User.findById(req.user._id).select('-password');

    // Get user statistics
    let stats = {};
    if (user.role === 'client') {
      const orderStats = await Order.aggregate([
        { $match: { client: user._id } },
        {
          $group: {
            _id: null,
            totalOrders: { $sum: 1 },
            totalSpent: { $sum: '$price' },
            pendingOrders: {
              $sum: { $cond: [{ $in: ['$status', ['pending', 'assigned', 'paid', 'in_progress']] }, 1, 0] }
            },
            completedOrders: {
              $sum: { $cond: [{ $eq: ['$status', 'completed'] }, 1, 0] }
            }
          }
        }
      ]);
      stats = orderStats[0] || { totalOrders: 0, totalSpent: 0, pendingOrders: 0, completedOrders: 0 };
    } else if (user.role === 'ishchi') {
      const workerStats = await Order.aggregate([
        { $match: { worker: user._id } },
        {
          $group: {
            _id: null,
            totalOrders: { $sum: 1 },
            totalEarned: { $sum: '$price' },
            activeOrders: {
              $sum: { $cond: [{ $in: ['$status', ['assigned', 'paid', 'in_progress']] }, 1, 0] }
            },
            completedOrders: {
              $sum: { $cond: [{ $eq: ['$status', 'completed'] }, 1, 0] }
            }
          }
        }
      ]);
      stats = workerStats[0] || { totalOrders: 0, totalEarned: 0, activeOrders: 0, completedOrders: 0 };
    }

    res.json({
      success: true,
      user: { ...user.toObject(), stats }
    });

  } catch (error) {
    console.error('Get profile error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Update user profile
router.put('/profile', async (req, res) => {
  try {
    const { username, phone, address } = req.body;
    const updateData = {};

    if (username) updateData.username = username;
    if (phone) updateData.phone = phone;
    if (address) updateData.address = address;

    // Check if username is already taken
    if (username) {
      const existingUser = await User.findOne({
        username,
        _id: { $ne: req.user._id }
      });
      if (existingUser) {
        return res.status(400).json({
          success: false,
          message: 'Bu username allaqachon band'
        });
      }
    }

    const user = await User.findByIdAndUpdate(
      req.user._id,
      updateData,
      { new: true, runValidators: true }
    ).select('-password');

    res.json({
      success: true,
      message: 'Profil muvaffaqiyatli yangilandi',
      user
    });

  } catch (error) {
    console.error('Update profile error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Deactivate user (Admin only)
router.patch('/:userId/deactivate', authorize('admin'), async (req, res) => {
  try {
    const user = await User.findByIdAndUpdate(
      req.params.userId,
      { isActive: false },
      { new: true }
    ).select('-password');

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'Foydalanuvchi topilmadi'
      });
    }

    res.json({
      success: true,
      message: 'Foydalanuvchi deaktivlashtirildi',
      user
    });

  } catch (error) {
    console.error('Deactivate user error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Activate user (Admin only)
router.patch('/:userId/activate', authorize('admin'), async (req, res) => {
  try {
    const user = await User.findByIdAndUpdate(
      req.params.userId,
      { isActive: true },
      { new: true }
    ).select('-password');

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'Foydalanuvchi topilmadi'
      });
    }

    res.json({
      success: true,
      message: 'Foydalanuvchi aktivlashtirildi',
      user
    });

  } catch (error) {
    console.error('Activate user error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Get dashboard statistics (Admin only)
router.get('/dashboard/stats', authorize('admin'), async (req, res) => {
  try {
    // Get user statistics
    const userStats = await User.aggregate([
      {
        $group: {
          _id: '$role',
          count: { $sum: 1 },
          active: { $sum: { $cond: ['$isActive', 1, 0] } }
        }
      }
    ]);

    // Get order statistics
    const orderStats = await Order.aggregate([
      {
        $group: {
          _id: '$status',
          count: { $sum: 1 },
          totalValue: { $sum: '$price' }
        }
      }
    ]);

    // Get monthly order trends
    const monthlyStats = await Order.aggregate([
      {
        $group: {
          _id: {
            year: { $year: '$createdAt' },
            month: { $month: '$createdAt' }
          },
          orders: { $sum: 1 },
          revenue: { $sum: '$price' }
        }
      },
      { $sort: { '_id.year': -1, '_id.month': -1 } },
      { $limit: 12 }
    ]);

    // Get service popularity
    const serviceStats = await Order.aggregate([
      {
        $group: {
          _id: '$service',
          count: { $sum: 1 },
          revenue: { $sum: '$price' }
        }
      },
      { $sort: { count: -1 } }
    ]);

    res.json({
      success: true,
      stats: {
        users: userStats,
        orders: orderStats,
        monthly: monthlyStats.reverse(),
        services: serviceStats
      }
    });

  } catch (error) {
    console.error('Dashboard stats error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

module.exports = router;
