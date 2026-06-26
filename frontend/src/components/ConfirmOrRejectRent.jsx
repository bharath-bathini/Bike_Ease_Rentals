import React, { useState } from 'react';
import axios from 'axios';
import '../css/ConfirmOrRejectRent.css';

const ConfirmOrRejectRent = ({ rentId, onStatusChange }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAction = (action) => {
    setLoading(true);
    setError('');

    axios
      .post(
        'http://127.0.0.1:8000/api/confirm_or_reject_rent',
        { rent_id: rentId, action },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        }
      )
      .then((response) => {
        setLoading(false);
        onStatusChange(action); // Call the callback to update parent component
        alert(response.data.message);
      })
      .catch((error) => {
        setLoading(false);
        setError(error.response ? error.response.data.error : 'Something went wrong');
      });
  };

  return (
    <div className="confirm-reject-container">
      <h2>Confirm or Reject Rent</h2>
      <div className="button-container">
        <button
          className="confirm-btn"
          onClick={() => handleAction('confirm')}
          disabled={loading}
        >
          {loading ? 'Confirming...' : 'Confirm Rent'}
        </button>
        <button
          className="reject-btn"
          onClick={() => handleAction('reject')}
          disabled={loading}
        >
          {loading ? 'Rejecting...' : 'Reject Rent'}
        </button>
      </div>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default ConfirmOrRejectRent;
