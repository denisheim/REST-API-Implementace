// this module handles the MySQL connection setup.

const mysql = require('mysql2');

const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: '',
  database: 'rest_api'
});

const promisePool = pool.promise();

module.exports = promisePool;
