// src/App.jsx (請使用此程式碼替換舊的預設內容)

import React, { useState } from 'react';
import Login from './components/Login.jsx';
import ComplianceList from './components/ComplianceList.jsx';
import './App.css'; 

function App() {
  // 檢查 Local Storage 中是否有 Token 來初始化登入狀態
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem('authToken')
  );

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken'); // 從 Local Storage 移除 Token
    setIsAuthenticated(false);
  };

  return (
    <div className="app-main">
      <header>
          {/* 只有在登入狀態下才顯示登出按鈕 */}
          {isAuthenticated && (
              <button onClick={handleLogout} className="logout-button">登出</button>
          )}
      </header>

      {/* 根據 isAuthenticated 狀態進行條件渲染 */}
      {isAuthenticated ? (
        <ComplianceList /> // 已登入：顯示預警清單
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} /> // 未登入：顯示登入頁面
      )}
    </div>
  );
}

export default App;