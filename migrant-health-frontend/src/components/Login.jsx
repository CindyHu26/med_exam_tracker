import React, { useState } from 'react';
import { login } from '../api/auth';

function Login({ onLoginSuccess }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await login(username, password);
            // 登入成功，呼叫上層組件的成功處理函式，跳轉到數據頁面
            onLoginSuccess();
        } catch (err) {
            setError(err.message);
        }
    };

    // ... (加入您的 HTML 表單和 Material UI 組件來渲染登入介面) ...
}