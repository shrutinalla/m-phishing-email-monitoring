import { useState } from "react";
import { FaUser, FaLock, FaEye, FaEyeSlash } from "react-icons/fa";
import "./Login.css";

function Login() {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const [showPassword, setShowPassword] = useState(false);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");

    const handleSubmit = async (e) => {

        e.preventDefault();

        setLoading(true);

        setError("");

        console.log({
            username,
            password
        });

        setTimeout(() => {

            setLoading(false);

        },1500);

    }

    return (

        <div className="login-container">

            <div className="login-card">

                <div className="login-header">

                    <h1>MIDHANI</h1>

                    <p>Enterprise Phishing Awareness Platform</p>

                </div>

                <form onSubmit={handleSubmit}>

                    <div className="input-group">

                        <label>Username</label>

                        <div className="input-box">

                            <FaUser className="icon"/>

                            <input

                                type="text"

                                placeholder="Enter Username"

                                value={username}

                                onChange={(e)=>setUsername(e.target.value)}

                                required

                            />

                        </div>

                    </div>

                    <div className="input-group">

                        <label>Password</label>

                        <div className="input-box">

                            <FaLock className="icon"/>

                            <input

                                type={showPassword ? "text" : "password"}

                                placeholder="Enter Password"

                                value={password}

                                onChange={(e)=>setPassword(e.target.value)}

                                required

                            />

                            <span

                                className="eye"

                                onClick={()=>setShowPassword(!showPassword)}

                            >

                                {

                                    showPassword ?

                                    <FaEyeSlash/>

                                    :

                                    <FaEye/>

                                }

                            </span>

                        </div>

                    </div>

                    {

                        error &&

                        <div className="error">

                            {error}

                        </div>

                    }

                    <button

                        className="login-btn"

                        disabled={loading}

                    >

                        {

                            loading ?

                            "Signing In..."

                            :

                            "Login"

                        }

                    </button>

                </form>

                <div className="divider">

                    <span></span>

                    <p>Authorized Administrators Only</p>

                    <span></span>

                </div>

                <div className="footer">

                    MIDHANI Internship Project

                </div>

            </div>

        </div>

    )

}

export default Login;