import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from '../constants';
import '../css/BookingForm.css'; // Assuming you have a CSS file for styling
function BookingForm() {
    const { bikeId } = useParams();
    const [bike, setBike] = useState({});
    const [rentStartDate, setRentStartDate] = useState('');
    const [rentEndDate, setRentEndDate] = useState('');
    const [totalCost, setTotalCost] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/bikes/${bikeId}/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`,
            },
        })
            .then((response) => response.json())
            .then((data) => setBike(data))
            .catch((error) => console.log('Error fetching bike details:', error));
    }, [bikeId]);

    const handleRentDatesChange = (start, end) => {
        const startDate = new Date(start);
        const endDate = new Date(end);
        const timeDiff = endDate - startDate;
        const days = timeDiff / (1000 * 3600 * 24);
        const costPerDay = 20;
        if (days > 0) {
            setTotalCost(days * costPerDay);
        } else {
            setTotalCost(0);
        }
    };

    const handleBooking = (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('bike', bikeId);
        formData.append('rent_start_date', rentStartDate);
        formData.append('rent_end_date', rentEndDate);
        formData.append('total_cost', totalCost);

        fetch('http://127.0.0.1:8000/api/rents/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem(ACCESS_TOKEN)}`,
            },
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                alert('Booking successful:', data);
            })
            .catch((error) => console.log('Error booking bike:', error));
    };

    return (
        <div className="booking-form">
            <h2>Booking Form for {bike.bike_name}</h2>
            <form onSubmit={handleBooking}>
                <div>
                    <label>Rent Start Date</label>
                    <input
                        type="date"
                        placeholder="Start Date"
                        value={rentStartDate}
                        onChange={(e) => {
                            setRentStartDate(e.target.value);
                            handleRentDatesChange(e.target.value, rentEndDate);
                        }}
                        required
                    />
                </div>
                <div>
                    <label>Rent End Date</label>
                    <input
                        type="date"
                        placeholder="End Date"
                        value={rentEndDate}
                        onChange={(e) => {
                            setRentEndDate(e.target.value);
                            handleRentDatesChange(rentStartDate, e.target.value);
                        }}
                        required
                    />
                </div>
                <div>
                    <label>Total Cost: ${totalCost}</label>
                </div>
                <button type="submit">Confirm Booking</button>
            </form>
        </div>
    );
}

export default BookingForm;
