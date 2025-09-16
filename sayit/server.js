const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const socketIO = require('socket.io');
const http = require('http');
require('dotenv').config();

const authRoutes = require('./routes/auth');
const orderRoutes = require('./routes/orders');
const paymentRoutes = require('./routes/payments');
const userRoutes = require('./routes/users');
const { authenticateToken } = require('./middleware/auth');

const app = express();
const server = http.createServer(app);
const io = socketIO(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

// Middleware
app.use(helmet());
app.use(morgan('combined'));
app.use(cors());
app.use(express.json());

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use(limiter);

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/service_orders', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

mongoose.connection.on('connected', () => {
  console.log('MongoDB ga muvaffaqiyatli ulandi');
});

mongoose.connection.on('error', (err) => {
  console.error('MongoDB xatosi:', err);
});

// WebSocket connection handling
const connectedUsers = new Map();

io.on('connection', (socket) => {
  console.log('Yangi foydalanuvchi ulandi:', socket.id);

  socket.on('join', (userId) => {
    connectedUsers.set(userId, socket.id);
    socket.join(userId);
    console.log(`Foydalanuvchi ${userId} qo'shildi`);
  });

  socket.on('disconnect', () => {
    for (const [userId, socketId] of connectedUsers.entries()) {
      if (socketId === socket.id) {
        connectedUsers.delete(userId);
        break;
      }
    }
    console.log('Foydalanuvchi uzildi:', socket.id);
  });
});

// Make io available to routes
app.set('socketio', io);
app.set('connectedUsers', connectedUsers);

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/orders', authenticateToken, orderRoutes);
app.use('/api/payments', authenticateToken, paymentRoutes);
app.use('/api/users', authenticateToken, userRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    message: 'Server xatosi yuz berdi',
    error: process.env.NODE_ENV === 'development' ? err.message : 'Ichki server xatosi'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    success: false,
    message: 'API endpoint topilmadi'
  });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server ${PORT} portda ishlamoqda`);
});