import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [users, setUsers] = useState([]);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/users`);
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users', error);
      setError(error.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const url = isEditing 
        ? `${API_BASE_URL}/users/${editingUser.id}`
        : `${API_BASE_URL}/users`;

      const method = isEditing ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `Failed to ${isEditing ? 'update' : 'create'} user`);
      }

      fetchUsers();
      resetForm();
    } catch (error) {
      console.error(`Error ${isEditing ? 'updating' : 'creating'} user`, error);
      setError(error.message);
    }
  };

  const handleEdit = (user) => {
    setEditingUser(user);
    setUsername(user.username);
    setEmail(user.email);
    setIsEditing(true);
    setError(null);
  };

  const handleDelete = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to delete user');
      }

      fetchUsers();
      setError(null);
    } catch (error) {
      console.error('Error deleting user', error);
      setError(error.message);
    }
  };

  const resetForm = () => {
    setUsername('');
    setEmail('');
    setEditingUser(null);
    setIsEditing(false);
    setError(null);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">User Management</h1>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="mb-4">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border p-2 mr-2 mb-2"
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2 mr-2 mb-2"
          required
        />
        <button 
          type="submit" 
          className="bg-blue-500 text-white p-2 rounded mr-2"
        >
          {isEditing ? 'Update User' : 'Add User'}
        </button>
        {isEditing && (
          <button 
            type="button" 
            onClick={resetForm}
            className="bg-gray-500 text-white p-2 rounded"
          >
            Cancel
          </button>
        )}
      </form>

      <div>
        <h2 className="text-xl font-semibold mb-2">Users</h2>
        {users.length === 0 ? (
          <p>No users found</p>
        ) : (
          <ul>
            {users.map((user) => (
              <li key={user.id} className="border-b py-2 flex justify-between items-center">
                <span>{user.username} ({user.email})</span>
                <div>
                  <button
                    onClick={() => handleEdit(user)}
                    className="bg-yellow-500 text-white p-2 rounded mr-2"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(user.id)}
                    className="bg-red-500 text-white p-2 rounded"
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default App;