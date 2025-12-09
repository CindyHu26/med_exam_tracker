import React, { useState } from 'react';
import { login } from '../api/auth'; // 導入登入函式

function Login({ onLoginSuccess }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false); // 新增載入狀態

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            await login(username, password);
            // 登入成功，呼叫上層組件的成功處理函式
            onLoginSuccess(); 
        } catch (err) {
            // 顯示來自 API 的錯誤訊息
            setError(err.message); 
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <h1>移工追蹤系統登入</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>帳號:</label>
                    <input 
                        type="text" 
                        value={username} 
                        onChange={(e) => setUsername(e.target.value)} 
                        disabled={loading}
                        required
                    />
                </div>
                <div>
                    <label>密碼:</label>
                    <input 
                        type="password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        disabled={loading}
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? '登入中...' : '登入'}
                </button>
                {error && <p style={{ color: 'red' }}>{error}</p>}
            </form>
        </div>
    );
}

export default Login;