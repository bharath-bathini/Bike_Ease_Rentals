import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';  // Import Link for navigation
import '../css/ViewBikes.css'; // Assuming you have a CSS file for styling
import { ACCESS_TOKEN } from '../constants';

function ViewNewBikes() {
    const [bikes, setBikes] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/bikes/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`,
            },
        })
            .then(response => response.json())
            .then(data => setBikes(data))
            .catch(error => console.log('Error fetching bikes:', error));
    }, []);

    return (
        <div className="bike-list">
            {bikes.length > 0 ? (
                bikes.map((bike) => (
                    <div key={bike.id} className="bike-item">
                        <img
                            src={`http://127.0.0.1:8000${bike.bike_image}`}
                            alt={bike.bike_name}
                            className="bike-image"
                        />
                        <h3>{bike.bike_name} - {bike.registration_number}</h3>
                        <p>Model: {bike.bike_model}</p>
                        <p>Purchase Date: {bike.purchase_date}</p>
                        <p>Status: {bike.is_active ? 'Active' : 'Inactive'}</p>
                        <Link to={`/book/${bike.id}`}>
                            <button className="book-button">Book This Bike</button>
                        </Link>
                    </div>
                ))
            ) : (
                <p>No bikes found.</p>
            )}
        </div>
    );
}

export default ViewNewBikes;
