/**
 * listens on port 3000 and exposes endpoints:
 *   GET    /events/list
 *   POST   /events/save
 *   PATCH  /events/update
 *   DELETE /events/delete/:eventId
 * 
 * make sure to run "npm install express mysql2" first.
 */

const express = require('express');
const app = express();
const db = require('./db'); // import the promise-based pool

// use JSON body parser
app.use(express.json());

/**
 * GET /events/list
 * returns all events from the "events" table.
 */
app.get('/events/list', async (req, res) => {
  try {
    const [rows] = await db.query('SELECT * FROM events');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to retrieve events' });
  }
});

/**
 * POST /events/save
 * inserts a new event. Expects JSON with keys: id, name, time_start (required).
 * optional keys: description, time_end
 */
app.post('/events/save', async (req, res) => {
  const { id, name, time_start, description, time_end } = req.body;

  if (!id || !name || !time_start) {
    return res.status(400).json({ error: 'Missing required data' });
  }

  try {
    const query = `
      INSERT INTO events (id, name, description, time_start, time_end)
      VALUES (?, ?, ?, ?, ?)
    `;
    await db.query(query, [id, name, description || null, time_start, time_end || null]);
    res.json({ message: 'Event has been successfully added' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to save event' });
  }
});

/**
 * PATCH /events/update
 * partially updates an event identified by its "id".
 * expects JSON that must contain at least "id", plus any fields to update.
 */
app.patch('/events/update', async (req, res) => {
  const { id, name, description, time_start, time_end } = req.body;

  if (!id) {
    return res.status(400).json({ error: 'ID is required to update an event' });
  }

  let sql = 'UPDATE events SET ';
  const updates = [];
  const params = [];

  if (name !== undefined) {
    updates.push('name = ?');
    params.push(name);
  }
  if (description !== undefined) {
    updates.push('description = ?');
    params.push(description);
  }
  if (time_start !== undefined) {
    updates.push('time_start = ?');
    params.push(time_start);
  }
  if (time_end !== undefined) {
    updates.push('time_end = ?');
    params.push(time_end);
  }

  if (updates.length === 0) {
    return res.status(400).json({ error: 'No fields to update' });
  }

  sql += updates.join(', ');
  sql += ' WHERE id = ?';
  params.push(id);

  try {
    const [result] = await db.query(sql, params);
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Event not found' });
    }
    res.json({ message: 'Event updated successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to update event' });
  }
});

/**
 * DELETE /events/delete/:eventId
 * deletes an event by its ID.
 */
app.delete('/events/delete/:eventId', async (req, res) => {
  const { eventId } = req.params;

  try {
    const [result] = await db.query('DELETE FROM events WHERE id = ?', [eventId]);
    if (result.affectedRows === 0) {
      return res.status(404).json({ error: 'Event not found' });
    }
    res.json({ message: 'Event successfully deleted' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to delete event' });
  }
});

// start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Node.js server is running on http://localhost:${PORT}`);
});
