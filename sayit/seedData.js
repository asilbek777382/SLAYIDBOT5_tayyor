const mongoose = require('mongoose');
const User = require('./models/User');
require('dotenv').config();

const seedUsers = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/service_orders');

    // Create admin user
    const adminUser = new User({
      username: 'admin',
      email: 'admin@example.com',
      password: 'admin123',
      role: 'admin',
      phone: '+998901234567',
      address: 'Toshkent, Uzbekiston'
    });

    // Create sample workers
    const workers = [
      {
        username: 'plumber_ali',
        email: 'ali@plumber.com',
        password: 'worker123',
        role: 'ishchi',
        specialization: 'plumber',
        phone: '+998902345678',
        address: 'Toshkent'
      },
      {
        username: 'electrician_bobur',
        email: 'bobur@electric.com',
        password: 'worker123',
        role: 'ishchi',
        specialization: 'electrician',
        phone: '+998903456789',
        address: 'Toshkent'
      },
      {
        username: 'cleaner_malika',
        email: 'malika@clean.com',
        password: 'worker123',
        role: 'ishchi',
        specialization: 'cleaner',
        phone: '+998904567890',
        address: 'Toshkent'
      }
    ];

    // Create sample clients
    const clients = [
      {
        username: 'client_aziz',
        email: 'aziz@client.com',
        password: 'client123',
        role: 'client',
        phone: '+998905678901',
        address: 'Mirzo Ulugbek tumani, Toshkent'
      },
      {
        username: 'client_nodira',
        email: 'nodira@client.com',
        password: 'client123',
        role: 'client',
        phone: '+998906789012',
        address: 'Yunusobod tumani, Toshkent'
      }
    ];

    // Clear existing users
    await User.deleteMany({});

    // Save admin
    await adminUser.save();
    console.log('Admin foydalanuvchi yaratildi');

    // Save workers
    for (const workerData of workers) {
      const worker = new User(workerData);
      await worker.save();
      console.log(`${workerData.specialization} ishchisi yaratildi: ${workerData.username}`);
    }

    // Save clients
    for (const clientData of clients) {
      const client = new User(clientData);
      await client.save();
      console.log(`Mijoz yaratildi: ${clientData.username}`);
    }

    console.log('Barcha test foydalanuvchilar muvaffaqiyatli yaratildi!');
    console.log('\nLogin ma\'lumotlari:');
    console.log('Admin: admin@example.com / admin123');
    console.log('Plumber: ali@plumber.com / worker123');
    console.log('Electrician: bobur@electric.com / worker123');
    console.log('Cleaner: malika@clean.com / worker123');
    console.log('Client 1: aziz@client.com / client123');
    console.log('Client 2: nodira@client.com / client123');

    process.exit(0);
  } catch (error) {
    console.error('Seed xatosi:', error);
    process.exit(1);
  }
};

seedUsers();