#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
API服务器，为前端提供接口
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.coordinator import AnalysisCoordinator

# 创建FastAPI应用
app = FastAPI(title="行业分析API", version="1.0.0")

# 添加CORS中间件，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 允许前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量，存储分析协调器实例
coordinator = None

# 行业映射
INDUSTRY_MAPPING = {
    "new-energy-vehicle": "新能源汽车",
    "ai-tech": "人工智能",
    "healthcare": "医疗健康",
    "manufacturing": "智能制造",
    "aerospace": "航空航天",
    "ecommerce": "电子商务",
    "realestate": "房地产",
    "finance": "金融服务",
    "logistics": "物流运输"
}

# 请求模型
class AnalysisRequest(BaseModel):
    industry_id: str
    focus_areas: Optional[list] = None

class AnalysisStatus(BaseModel):
    status: str
    message: str
    progress: Optional[int] = None

# 全局变量，存储分析状态
analysis_status = {
    "status": "idle",
    "message": "",
    "progress": 0,
    "results": None
}

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化协调器"""
    global coordinator
    try:
        coordinator = AnalysisCoordinator()
        print("分析协调器初始化成功")
    except Exception as e:
        print(f"初始化分析协调器失败: {str(e)}")

@app.get("/")
async def root():
    """根路径"""
    return {"message": "行业分析API服务"}

@app.post("/api/analyze", response_model=AnalysisStatus)
async def start_analysis(request: AnalysisRequest):
    """开始分析"""
    global analysis_status, coordinator
    
    # 检查是否已有分析在进行
    if analysis_status["status"] == "running":
        return AnalysisStatus(
            status="error",
            message="已有分析任务在进行中，请稍后再试"
        )
    
    # 验证行业ID
    if request.industry_id not in INDUSTRY_MAPPING:
        raise HTTPException(status_code=400, detail=f"无效的行业ID: {request.industry_id}")
    
    # 更新状态
    analysis_status["status"] = "running"
    analysis_status["message"] = f"正在分析{INDUSTRY_MAPPING[request.industry_id]}行业..."
    analysis_status["progress"] = 10
    
    try:
        # 加载数据
        load_results = coordinator.load_data()
        analysis_status["progress"] = 30
        
        # 运行分析
        focus_areas = request.focus_areas if request.focus_areas else ["宏观经济", "财务", "市场"]
        analysis_results = coordinator.run_analysis(focus_areas)
        analysis_status["progress"] = 70
        
        # 生成报告
        report_results = coordinator.agents["ReportAgent"].run(analysis_results)
        analysis_status["progress"] = 90
        
        # 保存结果
        saved_files = coordinator.save_results()
        analysis_status["progress"] = 100
        
        # 更新状态
        analysis_status["status"] = "completed"
        analysis_status["message"] = "分析完成"
        analysis_status["results"] = {
            "report": report_results,
            "saved_files": saved_files
        }
        
        return AnalysisStatus(
            status="success",
            message="分析完成",
            progress=100
        )
        
    except Exception as e:
        analysis_status["status"] = "error"
        analysis_status["message"] = f"分析失败: {str(e)}"
        
        return AnalysisStatus(
            status="error",
            message=f"分析失败: {str(e)}"
        )

@app.get("/api/status")
async def get_status():
    """获取分析状态"""
    return analysis_status

@app.get("/api/results")
async def get_results():
    """获取分析结果"""
    if analysis_status["status"] != "completed":
        raise HTTPException(status_code=400, detail="分析尚未完成")
    
    return analysis_status["results"]

@app.get("/api/industries")
async def get_industries():
    """获取所有行业列表"""
    return [
        {"id": key, "name": value} 
        for key, value in INDUSTRY_MAPPING.items()
    ]

@app.get("/download")
async def download_file(file: str):
    """下载文件"""
    try:
        # 确保文件路径安全
        file_path = Path(file)
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        return FileResponse(
            path=str(file_path),
            filename=file_path.name,
            media_type='application/octet-stream'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载文件失败: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)