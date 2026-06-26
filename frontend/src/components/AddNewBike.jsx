import React, { useState } from 'react';
import { ACCESS_TOKEN } from '../constants';
import '../css/AddBikes.css'; // Assuming you have a CSS file for styling

function AddNewBike() {
    const [bikeData, setBikeData] = useState({
        bike_name: '',
        bike_model: '',
        registration_number: '',
        purchase_date: '',
        is_active: true,
        bike_image: null,
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setBikeData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleImageChange = (e) => {
        setBikeData((prevData) => ({
            ...prevData,
            bike_image: e.target.files[0],
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const formData = new FormData();
        for (const key in bikeData) {
            formData.append(key, bikeData[key]);
        }
    
        fetch('http://127.0.0.1:8000/api/bikes/add/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`,
            },
            body: formData, // No need to set Content-Type
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to add bike');
                }
                return response.json();
            })
            .then((data) => {
                alert('Bike added successfully!');
            })
            .catch((error) => {
                alert('Error adding bike: ' + error.message);
                console.error('Error adding bike:', error);
            });
    };
    

    return (
        <div className="add-bike-form-container">
            <h2>Add New Bike</h2>
            <form onSubmit={handleSubmit} className="add-bike-form">
                <div className="form-group">
                    <label htmlFor="bike_name">Bike Name</label>
                    <input
                        type="text"
                        id="bike_name"
                        name="bike_name"
                        value={bikeData.bike_name}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="bike_model">Bike Model</label>
                    <input
                        type="text"
                        id="bike_model"
                        name="bike_model"
                        value={bikeData.bike_model}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="registration_number">Registration Number</label>
                    <input
                        type="text"
                        id="registration_number"
                        name="registration_number"
                        value={bikeData.registration_number}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="purchase_date">Purchase Date</label>
                    <input
                        type="date"
                        id="purchase_date"
                        name="purchase_date"
                        value={bikeData.purchase_date}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="is_active">Status</label>
                    <input
                        type="checkbox"
                        id="is_active"
                        name="is_active"
                        checked={bikeData.is_active}
                        onChange={() => setBikeData({ ...bikeData, is_active: !bikeData.is_active })}
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="bike_image">Bike Image</label>
                    <input
                        type="file"
                        id="bike_image"
                        name="bike_image"
                        onChange={handleImageChange}
                        accept="image/*"
                    />
                </div>
                <button type="submit" className="submit-button">Add Bike</button>
            </form>
        </div>
    );
}

export default AddNewBike;
