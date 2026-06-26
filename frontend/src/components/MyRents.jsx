import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../css/MyRents.css';
import { ACCESS_TOKEN } from '../constants';

const MyRents = () => {
  const [rents, setRents] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/my-rents/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`
      }
    })
    .then(response => {
      setRents(response.data);
    })
    .catch(error => {
      console.error('Error fetching rents:', error);
    });
  }, []);

  return (
    <div className="rents-container">
      <h2>My Rents</h2>
      {rents.length === 0 ? (
        <p>No rentals found.</p>
      ) : (
        <table className="rents-table">
          <thead>
            <tr>
              <th>Bike Name</th>
              <th>Start Date</th>
              <th>End Date</th>
              <th>Price/Day</th>
              <th>Total Price</th>
            </tr>
          </thead>
          <tbody>
            {rents.map((rent) => (
              <tr key={rent.id}>
                <td>{rent.bike_name}</td>
                <td>{rent.rent_start_date}</td>
                <td>{rent.rent_end_date}</td>
                <td>₹{rent.price_per_day}</td>
                <td>₹{rent.total_price}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default MyRents;
