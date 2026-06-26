import React, { useState } from 'react'
import '../css/Home.css';
import '../css/Register.css'
import axios from 'axios';
export const Register = () => {
    const [Confirmpassword,setConfirmpassword]=useState('');
    const [formData,setformData]=useState({
        username:'',
        password:'',
        email:'',
    })
    const [loading ,setLoading]=useState(false);
    const [status,setstatus]=useState('');
    const handleChanges=(e)=>{
        const {name,value}=e.target;
        setformData({
          ...formData,
          [name]:value,
        })
      }
      const handleSubmit=async(e)=>{
        setLoading(true);
        e.preventDefault();
        try{
          if (Confirmpassword === formData.password){
            const response = await axios.post('http://127.0.0.1:8000/api/signup/',formData);
            setstatus(response.data.message);
            setformData({
              username :'',
              email:'',
              password:'',
              first_name:''
            });
          }
          else{
            setstatus('password Not match')
          }
        }catch(error){
          setstatus('Registration Failed',error)
        }finally{
          setLoading(false)
        }
      }
  return (
    <div>
        <div classNameName='content'>
            <h1>BikeEase: Efficient management system for bike rentals and user convenience </h1>
        </div>
        <div className="inFormBackground">
            <div className="inSignForm">
                <h2>New Sign up</h2>
                {status && <p className='message'>{status}</p>}
                <form onSubmit={handleSubmit} method="post">
                    <div className="form-columns column">
                        <div className="inputGroup">
                            <label htmlFor="name">Name</label>
                            <input type="text" id="name" name="name" placeholder="Enter Name" value={formData.first_name} onChange={handleChanges} required />
                        </div>
                        <div className="inputGroup">
                            <label htmlFor="mobile">Mobile</label>
                            <input type="tel" id="mobile" name="mobile" placeholder="Enter Mobile Number" required />
                        </div>
                        <div className="inputGroup">
                            <label htmlFor="email">Email</label>
                            <input type="email" id="email" name="email" placeholder="Enter Email" value={formData.email} onChange={handleChanges}  required />
                        </div>
                        <div className="inputGroup">
                            <label htmlFor="username">Username</label>
                            <input type="text" id="username" name="username" placeholder="Enter Username"  minlength="4" value={formData.username} onChange={handleChanges}  required />
                        </div>
                        <div className="inputGroup">
                            <label htmlFor="password">Password</label>
                            <input type="password" id="password" name="password" placeholder="Enter Password" pattern="^(?=.*[a-zA-Z])(?=.*\d).+$"  title="Password must be at least 8 characters long, and contain both letters and numbers." value={formData.password} onChange={handleChanges}  required />
                        </div>
                        <div className="inputGroup">
                            <label htmlFor="confirm-password">Confirm Password</label>
                            <input type="password" id="confirm-password" name="cnfm_password" placeholder="Enter Password" pattern="^(?=.*[a-zA-Z])(?=.*\d).+$" value={Confirmpassword} onChange={(e)=>setConfirmpassword(e.target.value)}  required />
                        </div>
                    </div>
                    <button className="submitForm" disabled={loading}>{ loading ? 'Signing Up please wait....':'Signup' }</button>
                </form>
            </div>
        </div>
    </div>
  )
}
