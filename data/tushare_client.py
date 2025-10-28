"""
Tushare数据客户端
用于获取A股市场数据
"""
import tushare as ts
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
import json

class TushareClient:
    """Tushare数据客户端"""
    
    def __init__(self, token: str):
        """初始化Tushare客户端"""
        self.token = token
        ts.set_token(token)
        self.pro = ts.pro_api()
        
    def get_stock_basic_info(self, ts_code: str) -> Optional[Dict[str, Any]]:
        """获取股票基本信息"""
        try:
            df = self.pro.stock_basic(ts_code=ts_code, fields='ts_code,name,area,industry,market,list_date')
            if df.empty:
                return None
            return df.iloc[0].to_dict()
        except Exception as e:
            print(f"❌ 获取股票基本信息失败: {e}")
            return None
    
    def get_daily_data(self, ts_code: str, days: int = 60) -> Optional[pd.DataFrame]:
        """获取日线行情数据"""
        try:
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
            
            df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            if df.empty:
                return None
            
            df = df.sort_values('trade_date')
            return df
        except Exception as e:
            print(f"❌ 获取日线数据失败: {e}")
            return None
    
    def get_financial_data(self, ts_code: str) -> Optional[Dict[str, Any]]:
        """获取财务数据"""
        try:
            # 获取最新财报
            end_date = datetime.now().strftime('%Y%m%d')
            
            # 利润表
            income_df = self.pro.income(ts_code=ts_code, end_date=end_date, fields='ts_code,end_date,total_revenue,revenue,operate_profit,total_profit,n_income')
            
            # 资产负债表
            balance_df = self.pro.balancesheet(ts_code=ts_code, end_date=end_date, fields='ts_code,end_date,total_assets,total_liab,total_hldr_eqy_exc_min_int')
            
            # 现金流量表
            cashflow_df = self.pro.cashflow(ts_code=ts_code, end_date=end_date, fields='ts_code,end_date,n_cashflow_act,n_cashflow_inv_act,n_cash_flows_fnc_act')
            
            result = {}
            if not income_df.empty:
                result['income'] = income_df.iloc[0].to_dict()
            if not balance_df.empty:
                result['balance'] = balance_df.iloc[0].to_dict()
            if not cashflow_df.empty:
                result['cashflow'] = cashflow_df.iloc[0].to_dict()
                
            return result if result else None
        except Exception as e:
            print(f"❌ 获取财务数据失败: {e}")
            return None
    
    def get_financial_indicators(self, ts_code: str) -> Optional[pd.DataFrame]:
        """获取财务指标"""
        try:
            end_date = datetime.now().strftime('%Y%m%d')
            df = self.pro.fina_indicator(ts_code=ts_code, end_date=end_date, 
                                         fields='ts_code,end_date,eps,roe,roa,gross_profit_margin,debt_to_assets,current_ratio,quick_ratio')
            return df if not df.empty else None
        except Exception as e:
            print(f"❌ 获取财务指标失败: {e}")
            return None
    
    def get_realtime_quote(self, ts_code: str) -> Optional[Dict[str, Any]]:
        """获取实时行情"""
        try:
            # 获取最新交易日数据
            end_date = datetime.now().strftime('%Y%m%d')
            df = self.pro.daily(ts_code=ts_code, trade_date=end_date)
            
            if df.empty:
                # 如果今天没有数据，获取最近一个交易日
                df = self.pro.daily(ts_code=ts_code, end_date=end_date)
                if df.empty:
                    return None
            
            latest = df.iloc[0].to_dict()
            return latest
        except Exception as e:
            print(f"❌ 获取实时行情失败: {e}")
            return None
    
    def get_news(self, ts_code: str, days: int = 7) -> Optional[list]:
        """获取新闻资讯"""
        try:
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
            
            df = self.pro.news(src='sina', start_date=start_date, end_date=end_date)
            
            if df.empty:
                return []
            
            # 简单过滤：查找包含股票代码或名称的新闻
            stock_info = self.get_stock_basic_info(ts_code)
            if stock_info:
                stock_name = stock_info.get('name', '')
                # 这里可以进一步优化新闻过滤逻辑
                
            return df.head(10).to_dict('records')
        except Exception as e:
            print(f"⚠️ 获取新闻数据失败（可能需要更高级别的Tushare权限）: {e}")
            return []
    
    def get_comprehensive_data(self, ts_code: str) -> Dict[str, Any]:
        """获取综合数据包"""
        print(f"\n📊 正在获取 {ts_code} 的综合数据...")
        
        data = {
            'ts_code': ts_code,
            'fetch_time': datetime.now().isoformat(),
            'basic_info': self.get_stock_basic_info(ts_code),
            'daily_data': None,
            'financial_data': self.get_financial_data(ts_code),
            'financial_indicators': None,
            'realtime_quote': self.get_realtime_quote(ts_code),
            'news': self.get_news(ts_code),
        }
        
        # 转换DataFrame为dict
        daily_df = self.get_daily_data(ts_code)
        if daily_df is not None:
            data['daily_data'] = daily_df.to_dict('records')
            
        indicators_df = self.get_financial_indicators(ts_code)
        if indicators_df is not None:
            data['financial_indicators'] = indicators_df.to_dict('records')
        
        print(f"✅ 数据获取完成")
        return data
    
    def save_data_to_cache(self, ts_code: str, data: Dict[str, Any], cache_dir: str = "data/cache"):
        """保存数据到缓存"""
        os.makedirs(cache_dir, exist_ok=True)
        filename = f"{cache_dir}/{ts_code}_{datetime.now().strftime('%Y%m%d')}.json"
        
        # 处理pandas对象
        def default_serializer(obj):
            if isinstance(obj, pd.Timestamp):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=default_serializer)
        
        print(f"💾 数据已缓存到: {filename}")
        return filename

