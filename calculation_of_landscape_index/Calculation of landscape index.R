library(landscapemetrics)
library(terra)
library(openxlsx)


##############################输入设置##############################

# 1.设置工作目录（用户需要根据自己的文件路径进行替换）
setwd("E:/a_R_RStudio/Projects/input_data")


# 2.读取土地覆盖数据文件（用户需要根据自己的文件名进行替换）
landscape <- terra::rast("NB_LandCover1.tif")

# 3.计算一些示例景观指数（用户可以根据需要添加或删除这些代码，相关景观指数函数可参考下方网址）
# https://github.com/r-spatialecology/landscapemetrics/blob/main/NAMESPACE
enn_results_test3_1 <- lsm_c_lsi(landscape)
enn_results_test3_2 <- lsm_l_shape_sd(landscape)
enn_results_test3_3 <- lsm_c_shape_sd(landscape)
enn_results_test1 <- lsm_c_lsi(landscape)
enn_results_test2 <- lsm_c_lsi(landscape)

# landscape[landscape == 0] <- -99
# plot(landscape1)



##############################结果保存##############################
# 定义要执行的景观度量方法
metrics_c <- list(
  LPI = lsm_c_lpi,
  AI = lsm_c_ai,
  CLUMMPY = lsm_c_clumpy,
  LSI = lsm_c_lsi,
  MPS = lsm_c_area_mn
  # 添加更多以 lsm_c 开头的函数
)

metrics_l <- list(
  PD = lsm_l_pd,
  LSI = lsm_l_lsi,
  CONTAG = lsm_l_contag,
  PRD = lsm_l_prd,
  PSSP = lsm_l_area_sd

  # 添加更多以 lsm_l 开头的函数
)

# 定义一个函数来保存结果到Excel
save_to_excel <- function(result, filename) {
  write.xlsx(list("Sheet1" = as.data.frame(result)), filename)
}

# 循环执行每个以 lsm_c 开头的景观度量方法并保存结果
for (metric_name in names(metrics_c)) {
  result <- metrics_c[[metric_name]](landscape)
  filename <- paste0("class_", metric_name, ".xlsx")
  save_to_excel(result, filename)
}

# 循环执行每个以 lsm_l 开头的景观度量方法并保存结果
for (metric_name in names(metrics_l)) {
  result <- metrics_l[[metric_name]](landscape)
  filename <- paste0("landscape_", metric_name, ".xlsx")
  save_to_excel(result, filename)
}







