// src/components/ComplianceList.jsx
import React, { useState, useEffect } from 'react';
import { fetchComplianceData } from '../api/auth';

function ComplianceList() {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                const complianceList = await fetchComplianceData();
                setData(complianceList);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        loadData();
    }, []);

    if (loading) return <div>載入中...</div>;
    if (error) return <div style={{ color: 'red' }}>錯誤：{error}</div>;

    return (
        <div>
            <h1>移工體檢預警清單</h1>
            {data.length === 0 ? (
                <p>恭喜，目前沒有需要警示的移工。</p>
            ) : (
                // ... (使用 Material UI 的 Table 組件來顯示 data 內容) ...
                <ul>
                    {data.map(worker => (
                        <li key={worker.id}>
                            {worker.full_name} ({worker.employer_name}) - 
                            需要關注的週期: {worker.exam_statuses.filter(s => s.status !== '已合格').map(s => s.type).join(', ')}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}