import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faHome,
  faSignOutAlt,
  faUser,
  faBicycle,
  faClipboardList,
  faCreditCard,
  faUsers,
  faClipboardCheck,
  faHistory,
  faUserPlus,
  faSignInAlt,
} from '@fortawesome/free-solid-svg-icons';
import "../css/Header.css";

const Header = ({ isAuthenticated, admin }) => {
  let menuItems;
  if (isAuthenticated && admin) {
      menuItems = (
        <>
          <li>
            <Link to="/">
              <FontAwesomeIcon icon={faHome} />
              <span>Dashboard</span>
            </Link>
          </li>
          <li>
            <Link to="/manage-bikes">
              <FontAwesomeIcon icon={faBicycle} />
              <span>Manage Bikes</span>
            </Link>
          </li>
         
          <li>
            <Link to="/logout">
              <FontAwesomeIcon icon={faSignOutAlt} />
              <span>Logout</span>
            </Link>
          </li>
        </>
      );
  } else if (isAuthenticated && !admin) {
      menuItems = (
        <>
          <li>
            <Link to="/">
              <FontAwesomeIcon icon={faHome} />
              <span>Home</span>
            </Link>
          </li>
          <li>
            <Link to="/available-bikes">
              <FontAwesomeIcon icon={faBicycle} />
              <span>Available Bikes</span>
            </Link>
          </li>
          <li>
            <Link to="/my-rentals">
              <FontAwesomeIcon icon={faClipboardCheck} />
              <span>My Rentals</span>
            </Link>
          </li>
          <li>
            <Link to="/logout">
              <FontAwesomeIcon icon={faSignOutAlt} />
              <span>Logout</span>
            </Link>
          </li>
        </>
      );
  } else {
      menuItems = (
        <>
          <li>
            <Link to="/">
              <FontAwesomeIcon icon={faHome} />
              <span>Home</span>
            </Link>
          </li>
          <li>
            <Link to="/available-bikes">
              <FontAwesomeIcon icon={faBicycle} />
              <span>Browse Bikes</span>
            </Link>
          </li>
          <li>
            <Link to="/register">
              <FontAwesomeIcon icon={faUserPlus} />
              <span>Register</span>
            </Link>
          </li>
          <li>
            <Link to="/login">
              <FontAwesomeIcon icon={faSignInAlt} />
              <span>Login</span>
            </Link>
          </li>
        </>
      );
  }

  return (
    <div className="sidebar">
      <h2>{isAuthenticated ? "My Dashboard" : "Welcome"}</h2>
      <ul>{menuItems}</ul>
    </div>
  );
};

export default Header;