import akshare as ak
from typing import Annotated
from pandas import DataFrame
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

try:
    from .utils import save_output, SavePathType, decorate_all_methods, add_market_prefix, convert_symbol
except ImportError:
    from tradingagents.dataflows.utils import save_output, SavePathType, decorate_all_methods, add_market_prefix, convert_symbol


class AKShareIndexUtils:
    @staticmethod
    def get_index_data(
        index_code: Annotated[str, "指数代码"],
        start_date: Annotated[str, "开始日期，格式：YYYY-mm-dd"],
        end_date: Annotated[str, "结束日期，格式：YYYY-mm-dd"],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """获取指数历史数据
        
        Args:
            index_code: 指数代码 (如: "000001" 表示上证指数)
            start_date: 开始日期，格式：YYYY-mm-dd
            end_date: 结束日期，格式：YYYY-mm-dd
            save_path: 保存路径
            
        Returns:
            DataFrame: 指数历史数据
        """
        # 转换日期格式从 YYYY-mm-dd 到 YYYYMMDD
        start_date_formatted = start_date.replace('-', '')
        end_date_formatted = end_date.replace('-', '')
        
        try:
            # 获取指数历史数据
            index_data = ak.index_zh_a_hist(
                symbol=index_code,
                period="daily",
                start_date=start_date_formatted,
                end_date=end_date_formatted
            )
            
            # 检查返回数据是否为空
            if index_data is None or index_data.empty:
                print(f"无法获取指数 {index_code} 从 {start_date} 到 {end_date} 的数据")
                return DataFrame()
            
            # 转换列名以匹配统一格式
            index_data = index_data.rename(columns={
                '日期': 'Date',
                '开盘': 'Open',
                '最高': 'High',
                '最低': 'Low',
                '收盘': 'Close',
                '成交量': 'Volume',
                '成交额': 'Turnover',  # 成交额
                '涨跌幅': 'Change',    # 涨跌幅
                '涨跌额': 'Amount'     # 涨跌额
            })
            
            # 设置日期索引
            index_data['Date'] = pd.to_datetime(index_data['Date'])
            index_data = index_data.set_index('Date')
            
            # 添加 Adj Close 列（指数数据使用收盘价）
            index_data['Adj Close'] = index_data['Close']
            
            if save_path:
                save_output(index_data, f"Index data for {index_code}", save_path)
            
            return index_data
            
        except Exception as e:
            print(f"获取指数数据时出错: {str(e)}")
            return DataFrame()

    @staticmethod
    def get_major_indices_data(
        start_date: Annotated[str, "开始日期，格式：YYYY-mm-dd"],
        end_date: Annotated[str, "结束日期，格式：YYYY-mm-dd"],
        save_path: SavePathType = None,
    ) -> dict:
        """获取主要指数数据（上证指数、深证成指、创业板指）
        
        Args:
            start_date: 开始日期，格式：YYYY-mm-dd
            end_date: 结束日期，格式：YYYY-mm-dd
            save_path: 保存路径
            
        Returns:
            dict: 包含各指数数据的字典
        """
        # 主要指数代码
        indices = {
            "上证指数": "000001",
            "深证成指": "399001",
            "创业板指": "399006",
            "沪深300": "000300",
        }
        
        result = {}
        for name, code in indices.items():
            index_data = AKShareIndexUtils.get_index_data(code, start_date, end_date)
            if not index_data.empty:
                result[name] = index_data
            else:
                print(f"未能获取{name}({code})的数据")
        
        if save_path and result:
            # 保存为Excel文件，每个指数一个工作表
            with pd.ExcelWriter(save_path) as writer:
                for name, data in result.items():
                    data.to_excel(writer, sheet_name=name)
            print(f"主要指数数据已保存到 {save_path}")
        
        return result

    @staticmethod
    def get_index_info(index_code: Annotated[str, "指数代码"]) -> dict:
        """获取指数基本信息
        
        Args:
            index_code: 指数代码
            
        Returns:
            dict: 指数基本信息
        """
        try:
            # 获取指数基本信息
            info = ak.index_stock_info()
            index_info = info[info['index_code'] == index_code]
            
            if index_info.empty:
                return {}
            
            # 转换为字典格式
            info_dict = index_info.iloc[0].to_dict()
            return {
                'code': info_dict.get('index_code', index_code),
                'name': info_dict.get('display_name', 'N/A'),
                'publisher': info_dict.get('publisher', 'N/A'),
                'category': info_dict.get('category', 'N/A'),
                'base_date': info_dict.get('base_date', 'N/A'),
                'base_point': info_dict.get('base_point', 'N/A')
            }
        except Exception as e:
            print(f"获取指数基本信息时出错: {str(e)}")
            return {}

    @staticmethod
    def get_index_component_stocks(index_code: Annotated[str, "指数代码"]) -> DataFrame:
        """获取指数成分股
        
        Args:
            index_code: 指数代码
            
        Returns:
            DataFrame: 指数成分股数据
        """
        try:
            # 获取指数成分股
            component_stocks = ak.index_stock_cons(index_code)
            
            if component_stocks is None or component_stocks.empty:
                return DataFrame()
            
            return component_stocks
        except Exception as e:
            print(f"获取指数成分股时出错: {str(e)}")
            return DataFrame()

if __name__ == "__main__":
    # 设置显示选项
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_rows', 30)
    pd.set_option('display.float_format', lambda x: '{:,.2f}'.format(x) if isinstance(x, (float, int)) else str(x))
    
    # 测试代码
    try:
        print("测试获取主要指数数据")
        
        # 获取最近30天的数据
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        print(f"\n获取从 {start_date} 到 {end_date} 的主要中国A股过去30天的指数数据:")
        major_indices = AKShareIndexUtils.get_major_indices_data(start_date, end_date)
        
        for name, data in major_indices.items():
            print(f"\n{name} 数据预览:")
            print(data.tail(30))
        
        print("\n测试获取指数基本信息:")
        sh_info = AKShareIndexUtils.get_index_info("000001")
        print(f"上证指数基本信息: {sh_info}")
        
        sz_info = AKShareIndexUtils.get_index_info("399001")
        print(f"深证成指基本信息: {sz_info}")
        
        gem_info = AKShareIndexUtils.get_index_info("399006")
        print(f"创业板指基本信息: {gem_info}")
        
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        print(traceback.format_exc())