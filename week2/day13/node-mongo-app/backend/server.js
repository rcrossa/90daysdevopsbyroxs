const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const app = express();

// Configurar CORS
app.use(cors({
  origin: 'http://localhost:5173',
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

mongoose.connect('mongodb://db:27017/mydb', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});

mongoose.connection.on('connected', () => {
  console.log('✅ Conectado a MongoDB');
});

mongoose.connection.on('error', (err) => {
  console.error('❌ Error MongoDB:', err);
});

app.get('/', (req, res) => {
  res.send('¡API conectada a MongoDB con Docker!');
});

app.listen(3000, () => console.log('🚀 Server running on port 3000'));