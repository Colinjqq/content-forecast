<div align="center">
  <img src="docs/logo.svg" alt="Content Forecast" width="720">
</div>
<h2 align="center">Content Forecast</h2>
<p align="center">
  <a href="README.md"><strong>简体中文</strong></a>
  &nbsp;·&nbsp;
  <a href="docs/README_EN.md"><strong>English</strong></a>
</p>
<p align="center">
  <a href="#-mine-your-own-quadrant"><img src="docs/badge.svg" alt="Mine Your Own Quadrant · 挖自己的矿" width="328"></a>
</p>
<p align="center">
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-v0.1.0-orange" alt="Version"></a>
&nbsp;
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
&nbsp;
  <a href="SKILL.md"><img src="https://img.shields.io/badge/host-Claude_Code_·_Codex-2ea44f" alt="Hosts"></a>
&nbsp;
  <a href="https://github.com/Colinjqq/Content-Forecast/stargazers"><img src="https://img.shields.io/github/stars/Colinjqq/Content-Forecast?style=social" alt="Stars"></a>
</p>
<p align="center">
  <em>你以为选题慢，是因为灵感不够。<strong>不是</strong>。

  是你的判断没人帮你记账、复盘、固化成方法。</em>
</p>
<p align="center">
  <em>AI 告诉你<strong>大家都在写什么</strong>。

  Content Forecast 告诉你<strong>有些选题只有你能写的好</strong>。</em>
</p>
🧭 What it actually does
Most creators waste time on the same wrong question:
  "What should I write next?" → scroll hot lists → copy someone else → ship
The bottleneck isn't inspiration. It's that your judgment never gets logged, never gets reviewed, never compounds.
Content Forecast rebuilds the loop from the bottom up — using your industry experience as the only starting point:
🧭 画四象限 → 🎯 组合选题 → 📝 审核文稿 → 🎬 拍摄指引 → 📈 发布前预测 → 📊 72h 对账
This isn't a content mill. It's a judgment mill — every piece turns a guess into a verified data point.
One month in = you have a quadrant map that's only yours.
Three months in = your judgment is 3–5× sharper than day one.
🌀 Origin
  I make content. The worst part isn't writing — it's picking what to write.
  Every week, time spent finding topics > time spent writing.
  I tried AI topic generators, viral breakdowns, hot-list chasing — none of them worked. They told me what everyone writes. None of them told me what I can write.
  The four-quadrant method flips the question: first map your own mine — what do you understand, what does the market understand — then dig from your quadrant.
  After a while I noticed: real hits aren't chased. They're dug up. The deeper you know your industry, the more there is to dig.
  The prediction part came later. With a quadrant map and history, why not predict: will this one land or flop? T+72h review turns the guess into a verified data point.
  Two months in — topic-finding time cut in half. Judgment accuracy climbs.
  — the creator (Colin)
⚖️ How it differs from other "topic tools"
      Others
      This
      AI 帮你选题
      AI 帮你看懂自己能讲什么
      追热点、拆爆款
      从你自己的矿里挖
      灵感和标题党
      可验证的预测 + 发布后对账
      一周一篇
      一周挖三篇你自己的
In one sentence: other tools help you "ship more." This helps you "know your mine."
🤔 Can't I just use ChatGPT / Doubao / DeepSeek?
Those are general assistants — they answer based on global average training, not your account. You ask "will this topic work?" — you get the average answer. Ask again tomorrow — same answer. It doesn't remember you. It doesn't change because of you.
This is your own ops expert — serving only your one account:
The topic map is built from your industry experience, not scraped from someone else's channel
Every publish gets logged + reviewed — judgment gets sharper with time (auto-compounding)
It remembers what hit, what flopped, and why — things ChatGPT forgets after the first reply
General AI helps everyone pick topics. This helps you pick yours.
🛡️ Why the loop actually compounds
🗺️ Quadrant map starts from you: not "what's trending" — "what do I understand × what does the market understand." Consensus / blind-spot / forward-looking / gold-mine. The map evolves as you ship.
🎯 Topic is a combination, not a copy: combine 2–3 concepts inside or across quadrants → generate questions. You mine, the data decides.
📝 Every script gets reviewed: before filming, the rubric scores the script. Before publishing, the prediction gets logged. Written down — so future-you can audit past-you.
📊 Every publish gets settled: 72 hours later, actual data in — error %, interval hit, hit/miss width. No more "I feel this one didn't land."
🪒 The rubric is a workbench, not a museum: dimensions that don't predict get refactored. Only what sharpens you stays.
📦 Install
git clone https://github.com/Colinjqq/Content-Forecast.git
cd Content-Forecast
The skill is the whole folder — keep references/, templates/, scripts/ together.
Codex (default-tested): copy the folder to ~/.codex/skills/content-forecast, reopen your session, call content-forecast. Or just point an agent at the downloaded SKILL.md.
Claude Code: copy to ~/.claude/skills/content-forecast, use in a fresh session. (Path not yet self-validated on this machine.)
Requires a host model with file I/O + Python 3 (stdlib only). Network access optional. The repo itself doesn't ship any model service — cost follows your agent/provider. GitHub web view won't run the skill.
🚀 First run
In your content working directory, open a skill-compatible agent and say:
用 Content Forecast 帮我建立行业四象限地图。我做……，我做过……，我希望吸引……
(or init content-forecast)
Five yes/no questions complete onboarding. Strongly recommend importing 5–10 historical pieces as your benchmark — without one, your first 5 predictions land at ±50% precision.
⚡ Daily use
初始化 content-forecast           → 建立四象限 + 导入历史
组合选题 <象限A> ∩ <象限B>         → 给我 3 个我能讲的题
审核文稿 scripts/<...>.md          → 按评分项打分 + 拍摄建议
预测定稿 scripts/<...>.md          → 写入发布前快照 + P10/P90 基线
已发布 https://...                  → 标记发布时间 + 等 72h
对账 videos/<...>/                 → 实际数据 vs 预测 → 误差表 + 命中率
升级评分 / 查看历史 / 找参考账号    → 维护你自己的方法论
📈 Star History
<a href="https://star-history.com/#Colinjqq/Content-Forecast&Date">
  <img src="docs/star-history.svg" alt="Star History Chart" width="720">
</a>
📜 License
MIT. Commercial use, modification, closed-source integration — all fine.
Content creators split into two kinds:
those who chase traffic, and those who mine their own.
This is the second kind.
AI won't replace your thinking.
But it can stop you from guessing from scratch, every time.
  Reading this README was predicted too.
Reading this README was predicted too.
