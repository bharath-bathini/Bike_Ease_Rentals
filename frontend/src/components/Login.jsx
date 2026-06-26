import React, { useState } from 'react';
import '../css/Login.css'
import { ACCESS_TOKEN,REFRESH_TOKEN,Admin } from '../constants';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
export const Login = ({setisAuthenticated,setadmin}) => {
    const [username,setusername]=useState('');
    const [password,setpassword]=useState('');
    const [error,seterror]=useState('');
    const [loading,setloading]=useState('');
    const navigate=useNavigate();
    const handleSubmit= async(e)=>{
        e.preventDefault()
        setloading(true)
        try{
            const response=await axios.post('http://127.0.0.1:8000/api/token/',{username:username,password:password})
            localStorage.setItem(ACCESS_TOKEN,response.data.access);
            localStorage.setItem(REFRESH_TOKEN,response.data.refresh);
            setisAuthenticated(true)
            if (response.data.user.is_staff){
                localStorage.setItem(Admin,response.data.user.is_staff)
                setadmin(true)
            }else{
                setadmin(false)
                localStorage.removeItem(Admin)
            }
            console.log(response)
            navigate('/')
        }catch(error){
            seterror('Invalid credentials')
        }finally{
            setloading(false)
        }
    }
  return (
     <div >
        <div className='content'>
            <h1 >BikeEase: Efficient management system for bike rentals and user convenience </h1>
        </div>
        <div className="inFormBackground">
            <div className="inLoginForm">
                <h2>Sign IN</h2>
                {error && <p className='message'>{error}</p>}
                <form onSubmit={handleSubmit}>
                    <div className="form-columns">
                        <div className="inputGroup">
                            <label htmlFor="username">Username</label>
                            <input type="text" id="username" name="username" placeholder="Enter Username" value={username} onChange={(e)=>setusername(e.target.value)} required />
                        </div>
                        <div className="inputGroup">
                            <label htmlFor="password">Password</label>
                            <input type="password" id="password" name="password" placeholder="Enter Password" value={password} onChange={(e)=>setpassword(e.target.value)} required />
                        </div>
                    </div>
                    <button className="submitForm" disabled={loading}>{loading ? 'loging in...':'Login'}</button>
                </form>
            </div>
        </div>
    </div>
  )
}
