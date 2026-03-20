"""
A股选股器 - Streamlit Web App
免费数据源：akshare
"""

import streamlit as st
import akshare as ak
import pandas as pd
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="A股选股器",
    page_icon="📈",
    layout="wide"
)

st.title("📈 A股智能选股器")
st.markdown("---")

# 侧边栏 - 筛选条件
st.sidebar.header("🎯 筛选条件")

# 缓存数据加载
@st.cache_data(ttl=3600)  # 缓存1小时
def load_stock_data():
    """获取A股股票数据"""
    try:
        # 获取A股实时行情
        df = ak.stock_zh_a_spot_em()
        return df
    except Exception as e:
        st.error(f"获取数据失败: {e}")
        return None

@st.cache_data(ttl=3600)
def load_stock_info():
    """获取股票详细信息（财务指标）"""
    try:
        # 获取股票财务数据
        df = ak.stock_financial_abstract_ths(symbol="全部A股")
        return df
    except Exception as e:
        st.warning(f"获取财务数据失败，将使用简化筛选: {e}")
        return None

# 主筛选条件
st.sidebar.subheader("📊 基础指标")

# 市值筛选（亿）
market_cap_min = st.sidebar.number_input("最小市值（亿元）", value=10, step=10)
market_cap_max = st.sidebar.number_input("最大市值（亿元）", value=5000, step=100)

# PE筛选
pe_min = st.sidebar.number_input("最小PE（TTM）", value=0, step=1)
pe_max = st.sidebar.number_input("最大PE（TTM）", value=100, step=5)

# 涨跌幅筛选
change_min = st.sidebar.number_input("最小涨跌幅（%）", value=-10.0, step=0.5)
change_max = st.sidebar.number_input("最大涨跌幅（%）", value=10.0, step=0.5)

# 换手率
turnover_min = st.sidebar.number_input("最小换手率（%）", value=0.0, step=0.5)

# 行业筛选
st.sidebar.subheader("🏭 行业选择")
industry_options = [
    "不限", "新能源", "半导体", "医药生物", "电子", "计算机",
    "银行", "非银金融", "房地产", "化工", "机械设备",
    "汽车", "电力设备", "国防军工", "有色金属", "传媒"
]
selected_industry = st.sidebar.selectbox("所属行业", industry_options)

# 排序选项
st.sidebar.subheader("📋 排序方式")
sort_by = st.sidebar.selectbox(
    "排序字段",
    ["最新价", "涨跌幅", "涨跌额", "成交量", "成交额", "振幅", "换手率"]
)
sort_order = st.sidebar.radio("排序方向", ["降序", "升序"])

# 加载数据按钮
if st.sidebar.button("🔄 加载最新数据", type="primary"):
    st.cache_data.clear()
    st.rerun()

# 主界面
st.markdown("### 📋 筛选结果")

# 加载数据
with st.spinner("正在加载A股数据..."):
    df = load_stock_data()

if df is not None and len(df) > 0:
    # 数据预处理
    # 统一列名（akshare的列名可能变化）
    column_mapping = {
        '代码': 'code',
        '名称': 'name',
        '最新价': 'price',
        '涨跌幅': 'change_pct',
        '涨跌额': 'change',
        '成交量': 'volume',
        '成交额': 'amount',
        '振幅': 'amplitude',
        '最高': 'high',
        '最低': 'low',
        '今开': 'open',
        '昨收': 'prev_close',
        '换手率': 'turnover',
        '市盈率-动态': 'pe',
        '市净率': 'pb',
        '总市值': 'market_cap',
        '流通市值': 'float_cap',
    }

    # 重命名列
    df = df.rename(columns=column_mapping)

    # 确保数值列是数字类型
    numeric_cols = ['price', 'change_pct', 'change', 'volume', 'amount', 
                    'amplitude', 'turnover', 'pe', 'pb', 'market_cap', 'float_cap']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 应用筛选条件
    filtered_df = df.copy()

    # 市值筛选
    if 'market_cap' in filtered_df.columns:
        # 市值单位转换（akshare返回的是元，转换为亿）
        filtered_df['market_cap_yi'] = filtered_df['market_cap'] / 1e8
        filtered_df = filtered_df[
            (filtered_df['market_cap_yi'] >= market_cap_min) & 
            (filtered_df['market_cap_yi'] <= market_cap_max)
        ]

    # PE筛选
    if 'pe' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['pe'] >= pe_min) & 
            (filtered_df['pe'] <= pe_max) &
            (filtered_df['pe'] > 0)  # 排除负PE
        ]

    # 涨跌幅筛选
    if 'change_pct' in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df['change_pct'] >= change_min) & 
            (filtered_df['change_pct'] <= change_max)
        ]

    # 换手率筛选
    if 'turnover' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['turnover'] >= turnover_min]

    # 行业筛选（如果能获取到行业数据）
    # 注意：akshare的基础数据可能没有行业字段，这里做个提示

    # 排序
    if sort_by in filtered_df.columns:
        ascending = sort_order == "升序"
        filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)

    # 显示结果统计
    st.markdown(f"**共筛选出 {len(filtered_df)} 只股票**")

    # 显示数据
    if len(filtered_df) > 0:
        # 选择显示的列
        display_cols = ['code', 'name', 'price', 'change_pct', 'change', 
                        'volume', 'amount', 'turnover', 'pe', 'pb']
        
        # 只显示存在的列
        available_cols = [col for col in display_cols if col in filtered_df.columns]
        result_df = filtered_df[available_cols].copy()

        # 格式化显示
        if 'change_pct' in result_df.columns:
            result_df['change_pct'] = result_df['change_pct'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "-")
        if 'turnover' in result_df.columns:
            result_df['turnover'] = result_df['turnover'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "-")
        if 'pe' in result_df.columns:
            result_df['pe'] = result_df['pe'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")
        if 'pb' in result_df.columns:
            result_df['pb'] = result_df['pb'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "-")

        # 表格显示
        st.dataframe(
            result_df,
            use_container_width=True,
            height=500
        )

        # 下载功能
        csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下载为CSV",
            data=csv,
            file_name=f"选股结果_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

        # Excel下载
        excel_buffer = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
        filtered_df.to_excel(excel_buffer, index=False)
        excel_buffer.close()
        
        with open('temp.xlsx', 'rb') as f:
            excel_data = f.read()
        
        st.download_button(
            label="📥 下载为Excel",
            data=excel_data,
            file_name=f"选股结果_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.warning("没有符合筛选条件的股票，请调整筛选条件")

else:
    st.error("未能获取到数据，请稍后重试")

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "数据来源：东方财富 | 更新时间：" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') +
    "</div>",
    unsafe_allow_html=True
)
