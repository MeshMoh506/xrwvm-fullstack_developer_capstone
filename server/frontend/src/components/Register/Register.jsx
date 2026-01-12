import React, { useState } from "react";
import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";
import close_icon from "../assets/close.png";

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");

  const gohome = () => {
    window.location.href = window.location.origin;
  };

  const register = async (e) => {
    e.preventDefault();

    const register_url = window.location.origin + "/djangoapp/registration";
    
    const res = await fetch(register_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userName,
        password,
        firstName,
        lastName,
        email,
      }),
    });

    const json = await res.json();

    if (json.status) {
      sessionStorage.setItem("username", json.userName);
      window.location.href = window.location.origin;
    } else if (json.error === "Already Registered") {
      alert("This username is already registered.");
      window.location.href = window.location.origin;
    }
  };

  return (
    <>
      {/* INLINE CSS */}
      <style>{`
        .register-wrapper {
          width: 100%;
          height: 100vh;
          display: flex;
          justify-content: center;
          align-items: center;
          background: #f5f7fa;
        }

        .register-card {
          width: 420px;
          background: white;
          padding: 32px;
          border-radius: 14px;
          box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
          animation: fadeIn 0.3s ease;
        }

        .register-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 25px;
        }

        .register-header h2 {
          font-size: 26px;
          font-weight: 600;
          margin: 0;
        }

        .close-btn {
          width: 28px;
          cursor: pointer;
          opacity: 0.7;
          transition: 0.2s;
        }

        .close-btn:hover {
          opacity: 1;
        }

        .register-form {
          display: flex;
          flex-direction: column;
          gap: 18px;
        }

        .input-group {
          display: flex;
          align-items: center;
          background: #f0f2f5;
          padding: 12px 14px;
          border-radius: 10px;
        }

        .input-group img {
          width: 22px;
          margin-right: 10px;
          opacity: 0.7;
        }

        .input-group input {
          border: none;
          outline: none;
          background: transparent;
          width: 100%;
          font-size: 15px;
        }

        .register-btn {
          margin-top: 10px;
          padding: 12px;
          background: #4a6cf7;
          color: white;
          border: none;
          border-radius: 10px;
          font-size: 16px;
          cursor: pointer;
          transition: 0.25s;
        }

        .register-btn:hover {
          background: #3a57d9;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>

      {/* PAGE CONTENT */}
      <div className="register-wrapper">
        <div className="register-card">
          <div className="register-header">
            <h2>Sign Up</h2>
            <img
              src={close_icon}
              alt="close"
              className="close-btn"
              onClick={gohome}
            />
          </div>

          <form onSubmit={register} className="register-form">
            <div className="input-group">
              <img src={user_icon} alt="" />
              <input
                type="text"
                placeholder="Username"
                onChange={(e) => setUserName(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <img src={user_icon} alt="" />
              <input
                type="text"
                placeholder="First Name"
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <img src={user_icon} alt="" />
              <input
                type="text"
                placeholder="Last Name"
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <img src={email_icon} alt="" />
              <input
                type="email"
                placeholder="Email"
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="input-group">
              <img src={password_icon} alt="" />
              <input
                type="password"
                placeholder="Password"
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            <button type="submit" className="register-btn">
              Create Account
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export default Register;