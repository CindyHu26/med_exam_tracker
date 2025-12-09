------ employers 雇主基本資料表 ------
CREATE TABLE employers (
    employer_id SERIAL PRIMARY KEY,              -- 主鍵：系統自動生成ID
    company_name VARCHAR(100) NOT NULL,          -- 雇主/公司名稱
    tax_id VARCHAR(20) UNIQUE NOT NULL,          -- 統一編號（唯一且非空）
    contact_person VARCHAR(50),                  -- 聯絡人
    phone VARCHAR(20),                           -- 聯絡電話
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- 紀錄建立時間
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP  -- 紀錄更新時間
);

COMMENT ON TABLE employers IS '雇主基本資料表，用於識別聘用移工的公司。';

------ workers 移工基本資料表 ------
CREATE TABLE workers (
    worker_id SERIAL PRIMARY KEY,                -- 主鍵：系統自動生成ID
    arc_number VARCHAR(20) UNIQUE NOT NULL,      -- 居留證號（或替代ID，唯一且非空）
    passport_number VARCHAR(20) NOT NULL,        -- 護照號碼
    full_name VARCHAR(100) NOT NULL,             -- 移工全名
    nationality VARCHAR(50),                     -- 國籍
    hire_date DATE NOT NULL,                     -- 僱用起始日期（計算體檢週期基準）
    
    -- 外鍵：連結到 employers.employer_id，ON DELETE RESTRICT 防止誤刪雇主紀錄
    employer_id INT NOT NULL REFERENCES employers(employer_id) ON DELETE RESTRICT,
    
    is_active BOOLEAN DEFAULT TRUE,              -- 狀態：是否仍在聘僱中
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 建立索引以加速查詢
CREATE INDEX idx_workers_arc_number ON workers (arc_number);
CREATE INDEX idx_workers_employer_id ON workers (employer_id);

COMMENT ON TABLE workers IS '移工基本資料表，包含居留證號、國籍及僱用日期。';

------ medical_exams 體檢紀錄表 ------
CREATE TABLE medical_exams (
    exam_id BIGSERIAL PRIMARY KEY,               -- 主鍵：使用BIGSERIAL以防紀錄過多
    
    -- 外鍵：連結到 workers.worker_id，ON DELETE CASCADE 在移工被刪除時，同步刪除其體檢紀錄
    worker_id INT NOT NULL REFERENCES workers(worker_id) ON DELETE CASCADE,
    
    exam_date DATE NOT NULL,                     -- 實際體檢日期
    
    -- 體檢類別：用於判斷是哪一個週期 (6個月, 18個月, 30個月)
    exam_type VARCHAR(20) NOT NULL CHECK (exam_type IN ('入境體檢', '6個月體檢', '18個月體檢', '30個月體檢', '其他')),
    
    -- 體檢報告狀態：用於追蹤是否合格
    report_status VARCHAR(20) NOT NULL CHECK (report_status IN ('合格', '不合格', '補檢中', '待審核', '已完成')),
    
    expiry_date DATE,                            -- 體檢有效期限
    hospital_name VARCHAR(100),                  -- 執行體檢的醫院名稱
    report_document_url TEXT,                    -- 體檢報告檔案的儲存URL或路徑
    
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 建立複合索引以加速查詢特定移工的體檢紀錄
CREATE INDEX idx_medical_exams_worker_id_type ON medical_exams (worker_id, exam_type);

COMMENT ON TABLE medical_exams IS '移工體檢紀錄表，包含體檢日期、類型和報告結果。';