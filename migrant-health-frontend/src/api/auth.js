// src/api/auth.js

import axios from 'axios';

// Django 後端基底 URL
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'; 

/**
 * 1. 登入函式：獲取 Token
 * @param {string} username 
 * @param {string} password 
 * @returns {Promise<string>} 成功則返回 Token
 */
export async function login(username, password) {
    try {
        const response = await axios.post(`${API_BASE_URL}/auth/token/`, {
            username: username,
            password: password,
        });

        // 成功後，Token 會在 response.data.token 中
        const token = response.data.token;
        
        // 將 Token 存入瀏覽器的 Local Storage (重要！)
        localStorage.setItem('authToken', token);
        
        return token;

    } catch (error) {
        // 處理登入失敗 (例如：帳號密碼錯誤)
        throw new Error('登入失敗，請檢查帳號和密碼。');
    }
}


/**
 * 2. 獲取預警數據函式：需要使用 Authorization Header
 * @returns {Promise<Array>} 成功則返回移工預警清單
 */
export async function fetchComplianceData() {
    // 從 Local Storage 取回 Token
    const token = localStorage.getItem('authToken');

    if (!token) {
        throw new Error('未找到身份驗證憑證，請先登入。');
    }

    try {
        const response = await axios.get(`${API_BASE_URL}/compliance/due/`, {
            headers: {
                // 這是成功的關鍵！注意 'Token' 後面有一個空格
                'Authorization': `Token ${token}` 
            }
        });
        
        // 返回移工預警清單 (一個陣列)
        return response.data; 

    } catch (error) {
        // 處理 API 存取失敗 (例如：401/403 權限不足)
        if (error.response && error.response.status === 403) {
            throw new Error('權限不足，請確保您的帳號具有管理員身份。');
        }
        throw new Error('獲取數據失敗。');
    }
}