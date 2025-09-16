# Service Order Management System

Xizmat buyurtma boshqaruv tizimi - JWT authentication, to'lov tizimi va real-time xabarlar bilan.

## Xususiyatlar

- **Authentication & Authorization**: JWT token bilan login/register
- **Role-based Access**: Client, Ishchi, Admin rollari
- **Payment Integration**: Fake Payme/Click to'lov tizimi
- **Real-time Notifications**: WebSocket orqali jonli xabarlar
- **Order Management**: Buyurtma yaratish, tayinlash, kuzatish
- **Admin Dashboard**: Statistika va foydalanuvchilarni boshqarish

## Texnologiyalar

- **Backend**: Node.js, Express.js
- **Database**: MongoDB, Mongoose
- **Authentication**: JWT
- **Real-time**: Socket.IO
- **Security**: Helmet, Rate limiting

## O'rnatish

1. Repository ni clone qiling
2. Dependencies o'rnating:
   ```bash
   npm install
   ```

3. `.env` fayl yarating:
   ```
   NODE_ENV=development
   PORT=3000
   MONGODB_URI=mongodb://localhost:27017/service_orders
   JWT_SECRET=your-super-secret-jwt-key
   ```

4. MongoDB ni ishga tushiring

5. Test ma'lumotlarni yuklang:
   ```bash
   npm run seed
   ```

6. Serverni ishga tushiring:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Ro'yxatdan o'tish
- `POST /api/auth/login` - Tizimga kirish

### Orders
- `GET /api/orders` - Buyurtmalar ro'yxati
- `POST /api/orders` - Yangi buyurtma yaratish
- `GET /api/orders/:id` - Buyurtma tafsilotlari
- `PATCH /api/orders/:id/assign` - Buyurtmani qabul qilish
- `PATCH /api/orders/:id/status` - Buyurtma holatini yangilash

### Payments
- `POST /api/payments/:orderId/pay` - To'lov amalga oshirish
- `GET /api/payments/history` - To'lov tarixi
- `GET /api/payments/:paymentId` - To'lov tafsilotlari

### Users
- `GET /api/users` - Barcha foydalanuvchilar (Admin)
- `GET /api/users/profile` - Foydalanuvchi profili
- `PUT /api/users/profile` - Profilni yangilash
- `GET /api/users/dashboard/stats` - Admin statistikasi

## Rollar va Ruxsatlar

### Client
- O'z buyurtmalarini yaratish va ko'rish
- To'lov amalga oshirish
- Buyurtma holatini kuzatish

### Ishchi
- O'z mutaxassisligi bo'yicha buyurtmalarni ko'rish
- Buyurtmalarni qabul qilish
- Buyurtma holatini yangilash

### Admin
- Barcha foydalanuvchilarni ko'rish va boshqarish
- Barcha buyurtmalarni ko'rish
- Tizim statistikasini ko'rish

## WebSocket Events

### Client Events
- `new_order` - Yangi buyurtma (Ishchilarga)
- `order_assigned` - Buyurtma tayinlandi (Clientga)
- `order_status_updated` - Buyurtma holati yangilandi
- `payment_success` - To'lov muvaffaqiyatli
- `payment_failed` - To'lov amalga oshmadi

## Xizmat Turlari va Narxlar

- **Plumber (Santexnik)**: 150,000 so'm
- **Electrician (Elektrchi)**: 200,000 so'm
- **Cleaner (Tozalovchi)**: 100,000 so'm
- **Carpenter (Duradgor)**: 300,000 so'm
- **Painter (Bo'yovchi)**: 250,000 so'm
- **Mechanic (Mexanik)**: 400,000 so'm

## Test Foydalanuvchilar

Seed script ishlagach quyidagi test foydalanuvchilar yaratiladi:

- **Admin**: admin@example.com / admin123
- **Plumber**: ali@plumber.com / worker123  
- **Electrician**: bobur@electric.com / worker123
- **Cleaner**: malika@clean.com / worker123
- **Client 1**: aziz@client.com / client123
- **Client 2**: nodira@client.com / client123

## Development

Development rejimida ishlatish uchun:

```bash
npm run dev
```
*/ client
      const clientSocketId = connectedUsers.get(order.client._id.toString());
      if (clientSocketId) {
        io.to(clientSocketId).emit('payment_success', {
          orderId: order._id,
          transactionId: payment.transactionId,
          amount: payment.amount,
          message: 'To\'lov muvaffaqiyatli amalga oshirildi'
        });
      }

      // Notify worker if assigned
      if (order.worker) {
        const workerSocketId = connectedUsers.get(order.worker.toString());
        if (workerSocketId) {
          io.to(workerSocketId).emit('order_paid', {
            orderId: order._id,
            message: 'Buyurtma uchun to\'lov qabul qilindi'
          });
        }
      }

      res.json({
        success: true,
        message: 'To\'lov muvaffaqiyatli amalga oshirildi',
        payment: {
          transactionId: payment.transactionId,
          amount: payment.amount,
          status: payment.status
        }
      });

    } else {
      payment.status = 'failed';
      payment.failureReason = paymentResult.failureReason;
      await payment.save();

      order.status = 'canceled';
      await order.save();

      // Notify