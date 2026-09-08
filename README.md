# Content Forecast
**Created by Colin · 先找到你能接住的问题，再预测与复盘内容表现。**

A creator-first AI skill for concept mapping, topic generation, script review, filming guidance, and view forecasting with post-publish reviews.

## 它做什么
自我介绍 → 身份相关举例与填词 → 持续更新四象限 → 组合选题并确认 → 用户交稿 → 审核与视频操作 → 定稿预测 → 发布后对账。

四象限使用“我懂不懂 × 其他人懂不懂”：共识区、盲区、前瞻区、金矿区。受众和同行统一归为其他人。先从自己的行业经验出发，不必追热点。概念可以在同象限或跨象限组合，组合生成问题，证据决定最后的结论。

## 快速体验
把本项目交给具备文件读写能力的 Agent，明确指定读取 `SKILL.md`，然后说：
> 用 Content Forecast 帮我建立行业四象限地图。我做……，我做过……，我希望吸引……。

继续可以说：
- 用共识区和金矿区组合3个我能讲的选题。
- 我选第二个问题。这是我写的文案，请审核并告诉我下一步怎么拍。
- 这是同账号发布72小时的数据，帮我建立播放基线。
- 为这份定稿保存发布前预测。
- 已发布，实际发布时间是……。
- 这是72小时结果，帮我对账。

## 安装
Skill 是整个文件夹，复制时保留 references、templates、scripts。首版以当前本地 Codex 为制作环境；其他宿主尚未完成实机兼容测试。

Codex：将文件夹复制到你当前版本配置的个人 skills 目录（本地环境为 `~/.codex/skills/content-forecast`），重新打开会话后调用 `content-forecast`。也可以先让 Agent 直接读取下载目录的 SKILL.md 做体验。

Claude Code：通常放到 `~/.claude/skills/content-forecast`，在新会话使用；此路径说明尚未在本项目中实机验证。

需要宿主模型和文件读写；数据计算需要 Python 3（仅标准库）。联网检索可选。开源包不包含模型服务，费用由所用 Agent/服务决定。GitHub 在线页面本身不会运行此 Skill。

## 示例与数据
完整示例见 [examples/walkthrough.md](examples/walkthrough.md)。历史数据格式见 [templates/history.csv](templates/history.csv)。个人记录保存在独立内容工作目录的 `content-forecast-data/`，不上传到公共仓库。

## 预测能做到什么
v0.1 使用可比历史作品中位数和P10/P90生成探索性基线；不是经过验证的爆款模型。不同平台、账号、指标与时间窗口分别统计。少于5条可比数据不输出数值预测。

保存发布前内容快照、时间、方法和基线；到期计算误差、区间命中和宽度。标题、封面与成片质量尚未纳入独立分析。数据多不代表必然预测准；本项目尚无前瞻真实发布准确率成绩。

## 维护与反馈
反馈请说明版本、宿主、复现步骤、预期与实际结果，并脱敏。可改进方向：更多真实前瞻案例、稳定的数据导入、平台兼容；不代表这些已经实现。

[更新记录](CHANGELOG.md) · [验证记录](VALIDATION.md)

## 致谢
参考 [cheat-on-content](https://github.com/XBuilderLAB/cheat-on-content) 的发布前预测与发布后对账思路。四象限概念组合方法由 Colin 提供。预测记录与计算脚本为本项目实现。

MIT License。若对你有用，欢迎 Star，也欢迎提交预测失败的案例帮助改进。
