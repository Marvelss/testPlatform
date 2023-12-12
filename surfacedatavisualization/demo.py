import pandas as pd

df = pd.read_excel('2266s.xlsx', header=None)
print(df.shape)
# 获取最大行或列,补全表格成方阵,使得显示的热力图中的方格为正方形
max_columns = max(df.shape[1], df.shape[0])
df_filled = df.reindex(range(max_columns))
df_filled = df_filled.fillna(0)
df_filled.to_excel('test.xlsx', index=False)
print(df_filled.shape)
