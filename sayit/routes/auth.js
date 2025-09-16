const express = require('express');
const jwt = require('jsonwebtoken');
const { body, validationResult } = require('express-validator');
const User = require('../models/User');
const router = express.Router();

// Register
router.post('/register', [
  body('username').isLength({ min: 3 }).withMessage('Username kamida 3 ta belgi bo\'lishi kerak'),
  body('email').isEmail().withMessage('Email noto\'g\'ri formatda'),
  body('password').isLength({ min: 6 }).withMessage('Parol kamida 6 ta belgi bo\'lishi kerak'),
  body('role').isIn(['client', 'ishchi']).withMessage('Role client yoki ishchi bo\'lishi kerak')
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

    const { username, email, password, role, specialization, phone, address } = req.body;

    // Check if user exists
    const existingUser = await User.findOne({
      $or: [{ email }, { username }]
    });

    if (existingUser) {
      return res.status(400).json({
        success: false,
        message: 'Foydalanuvchi allaqachon mavjud'
      });
    }

    // Validate specialization for workers
    if (role === 'ishchi' && !specialization) {
      return res.status(400).json({
        success: false,
        message: 'Ishchi uchun mutaxassislik talab qilinadi'
      });
    }

    const user = new User({
      username,
      email,
      password,
      role,
      specialization,
      phone,
      address
    });

    await user.save();

    const token = jwt.sign(
      { userId: user._id, role: user.role },
      process.env.JWT_SECRET || 'your-secret-key',
      { expiresIn: '7d' }
    );

    res.status(201).json({
      success: true,
      message: 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi',
      token,
      user
    });

  } catch (error) {
    console.error('Register error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

// Login
router.post('/login', [
  body('email').isEmail().withMessage('Email noto\'g\'ri formatda'),
  body('password').notEmpty().withMessage('Parol talab qilinadi')
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

    const { email, password } = req.body;

    const user = await User.findOne({ email, isActive: true });
    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Email yoki parol noto\'g\'ri'
      });
    }

    const isPasswordValid = await user.comparePassword(password);
    if (!isPasswordValid) {
      return res.status(401).json({
        success: false,
        message: 'Email yoki parol noto\'g\'ri'
      });
    }

    const token = jwt.sign(
      { userId: user._id, role: user.role },
      process.env.JWT_SECRET || 'your-secret-key',
      { expiresIn: '7d' }
    );

    res.json({
      success: true,
      message: 'Muvaffaqiyatli kirish',
      token,
      user
    });

  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({
      success: false,
      message: 'Server xatosi'
    });
  }
});

module.exports = router;