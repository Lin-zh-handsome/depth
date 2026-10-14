# 第三章 3.6 实验结果
## 3.6.1 实验平台和评价指标
两个Benchmark、五任务、三方法、三种子；固定预算见table3_1.csv。Best为周期评测最大值，具有择优偏差；Last10按时间取最终10保存点；跨种子样本标准差ddof=1。
## 3.6.2 五任务成功率比较
TODO：45-run矩阵完整数据到齐后引用table3_2_best.csv和table3_3_last10.csv。
## 3.6.3 GSA与TokenLearner递进式效果分析
TODO：module_deltas.csv。M0→M1包含Depth和GSA；M1→M2保持相同Depth/GSA。
## 3.6.4 空间注意力与时序关注可视化
TODO：独立checkpoint真实闭环轨迹、轴向GSA Query传播权重、8个Token空间权重；阶段名称来自环境事件或明确标注。
## 3.6.5 典型操作过程与失败案例
TODO：相同reset的M0/M1/M2成功和失败轨迹；正式成功率评测不采集完整注意力张量。
