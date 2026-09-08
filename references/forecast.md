# 发布前预测 v0.1
首版是基于历史样本的经验预测与校准工具，不是经训练验证的传播模型。不能把一套流程描述成已经准确的算法。

## 输入与同口径
使用 templates/history.csv 字段：id,platform,account,metric,window_hours,views,paid,comparable。
每行对应一个已到达统计窗口的历史作品。views 为该窗口时点数据，不用累计终身播放冒充72小时数据；未知时不纳入。metric 精确保留平台原指标，曝光/阅读/播放不可混算。paid 和 comparable 为 true/false。
用户确认可比范围（例如近期同类口播），保留失败和异常爆款，不依据结果挑样本。付费推广样本默认排除；当前计划推广则此模型不适用。多平台分别运行，不能套换算系数。
建议统计窗口72小时，可由用户提前另定。没有历史数据仍能做选题和脚本。

## 计算与判断
运行：`python3 <skill>/scripts/forecast.py baseline <history.csv> --platform <平台> --account <账号> --metric <指标> --window-hours 72`
仅对匹配样本计算中位数、P10/P90（线性插值），作为历史基线和经验播放范围。少于5条拒绝数字预测；5条起也只称探索性经验区间。没有校准成绩前，不把P10/P90称为未来80%置信区间或80%命中保证。样本越少越强调不稳定，样本多也不能自动视为准确。
检查脚本相对历史材料的受众匹配、个人证据、开头承诺、证据画面、内容形式和新颖性。逐项只使用“强 / 中 / 弱 / 未知”，并给出材料依据。定性说明预期偏上、持平或偏下；默认不凭这些描述改数字，也不把定性等级相加后映射为播放量。
如用户已有可验证的调整规则，可创建 forecast override JSON（point,low,high,reason），记录为独立 experimental-adjustment；原始基线始终保存。调整不是“置信度更高”。

## 锁定
运行 lock：传入基线 JSON、脚本路径、新的记录目录，确认目标未发布、未见真实数据。工具复制脚本并保存摘要、UTC时间、方法和基线；不覆盖已有记录。它是本地留档，不能宣称防篡改公证。公开展示可在发布前保留屏幕录像或公开记录，但不自动对外发布。
严格使用 templates/prediction-card.md 输出和保存预测卡。卡片必须同时包含平台、账号、指标、窗口、样本数、历史中位数、P10/P90、中心预测、预测区间、方向判断、校准版本、预测依据、上行因素、下行因素、不可观测因素、内容版本和锁定时间。未知字段写“未知”，不能省略。
修改稿件后保留旧预测，新建记录并在发布前明确选定哪个是主预测，不能看完结果再择优。

## 工具参数
下面的 `<skill>` 是本 Skill 安装目录，`<item>` 是全新的单条预测目录，真实使用时替换占位符。

```sh
python3 <skill>/scripts/forecast.py baseline history.csv --platform 抖音 --account colin --metric 播放 --window-hours 72 --out baseline.json
python3 <skill>/scripts/forecast.py lock baseline.json script.md <item> --unpublished-unseen
python3 <skill>/scripts/forecast.py publish <item> --at 2026-09-08T15:00:00+08:00 --video-id 唯一作品ID
python3 <skill>/scripts/forecast.py review <item> --at 2026-09-11T15:00:00+08:00 --views 1500
python3 <skill>/scripts/forecast.py report <工作目录>/content-forecast-data/items
```
日期和播放数仅为格式示例，必须替换为真实值。`--unpublished-unseen` 仅在目标尚未发布且当前上下文未见实际结果时使用。脚本只保存用户声明，不能自行验证平台状态。
