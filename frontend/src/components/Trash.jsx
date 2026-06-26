import React from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faHome,
  faBell,
  faCog,
  faSignOutAlt,
  faUser,
  faShoppingCart,
  faEye,
  faHeart,
  faCalendarAlt,
  faUserPlus,
  faSignInAlt,
} from "@fortawesome/free-solid-svg-icons";
import "../css/Header.css";

const Header = ({ isAuthenticated, admin }) => {
  let menuItems;

  if (isAuthenticated && admin) {
    menuItems = (
      <>
        <li>
          <Link to="/">
            <FontAwesomeIcon icon={faHome} />
            <span>Home</span>
          </Link>
        </li>
        <li>
          <Link to="/alerts">
            <FontAwesomeIcon icon={faBell} />
            <span>Recent Alert</span>
          </Link>
        </li>
        <li>
          <Link to="/settings">
            <FontAwesomeIcon icon={faCog} />
            <span>Settings</span>
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
          <Link to="/profile">
            <FontAwesomeIcon icon={faUser} />
            <span>Profile</span>
          </Link>
        </li>
        <li>
          <Link to="/sale-product">
            <FontAwesomeIcon icon={faShoppingCart} />
            <span>Sale Product</span>
          </Link>
        </li>
        <li>
          <Link to="/view-product">
            <FontAwesomeIcon icon={faEye} />
            <span>View Product</span>
          </Link>
        </li>
        <li>
          <Link to="/wishlist">
            <FontAwesomeIcon icon={faHeart} />
            <span>Wishlist</span>
          </Link>
        </li>
        <li>
          <Link to="/booking">
            <FontAwesomeIcon icon={faCalendarAlt} />
            <span>Booking</span>
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
    <div className="container">
      <div className="content">
        <h1>Buy and Sell Reservations</h1>
        <p className="tagline">
          Revolutionizing the reservation trading industry, creating access to
          coveted tables for all tastemakers.
        </p>
        <div className="offer">
          <p>
            Sign up now for <span className="highlight">$20 credit</span> and
            receive <span className="highlight">$10</span> for every friend you
            refer.
          </p>
        </div>
        <form className="signup-form">
          <input type="email" placeholder="Enter your email address" required />
          <input type="email" placeholder="Enter your email address" required />
          <button type="submit">Continue</button>
        </form>
        <p className="footer-text">You can sit with us.</p>
      </div>
    </div>
  );
};

export default Header;
/*body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f7f7f7;
}

.container {
  background: #fff;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 400px;
}

h1 {
  font-size: 24px;
  margin-bottom: 10px;
}

.tagline {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
}

.offer {
  background: #fffae6;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.highlight {
  color: #ff6600;
  font-weight: bold;
}

.signup-form input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.signup-form button {
  width: 100%;
  padding: 10px;
  background: #ff6600;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}
.signup-form button:hover {
  background: #e65c00;
}

.footer-text {
  font-size: 12px;
  color: #888;
  margin-top: 10px;
}

h1 {
  font-size: 24px;
  margin-bottom: 10px;
}

.tagline {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
}

.offer {
  background: #fffae6;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.highlight {
  color: #ff6600;
  font-weight: bold;
}

.signup-form input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.signup-form button {
  width: 100%;
  padding: 10px;
  background: #ff6600;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.signup-form button:hover {
  background: #e65c00;
}

.footer-text {
  font-size: 12px;
  color: #888;
  margin-top: 10px;
}
*/