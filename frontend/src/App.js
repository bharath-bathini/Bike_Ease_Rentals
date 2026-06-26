import {  BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import { Home } from './components/Home';
import { Login } from './components/Login';
import { Register } from './components/Register';
import { useState,useEffect } from 'react';
import { ACCESS_TOKEN } from './constants';
import { useNavigate } from 'react-router-dom';
import { Admin } from './constants';
import AddNewBike from './components/AddNewBike';
import ViewNewBikes from './components/ViewNewBike';
import BookingForm from './components/BookingForm';
import MyRents from './components/MyRents';
import ConfirmOrRejectRent from './components/ConfirmOrRejectRent';
function Logout({setisAuthenticated,setadmin}){
  const navigate=useNavigate();
  useEffect(()=>{
    localStorage.clear();
    setisAuthenticated(false);
    setadmin(false);
  },[setisAuthenticated,setadmin])
  navigate('/login')
  return null;
}
function App() {
  const [isAuthenticated, setisAuthenticated] = useState(!!localStorage.getItem(ACCESS_TOKEN));
  const [admin,setadmin]=useState(!!localStorage.getItem(Admin));
  return(
    <Router>
      <div className='flex'>
        <Header isAuthenticated={isAuthenticated} admin={admin} />
        <Routes>
          <Route path='' element={<Home/>}/>
          <Route path='login' element={<Login setisAuthenticated={setisAuthenticated} setadmin={setadmin}/>}/>
          <Route path='register' element={<Register/>}/>
          <Route path='manage-bikes' element={<AddNewBike/>}/>
          <Route path='available-bikes' element={<ViewNewBikes/>}/>
          <Route path="book/:bikeId" element={<BookingForm/>} />
          <Route path='my-rentals' element={<MyRents />}/>
          <Route path='approval' element={<ConfirmOrRejectRent/>} />
          <Route path='logout' element={< Logout setisAuthenticated={setisAuthenticated} setadmin={setadmin}/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
