# Meeting Notes
Turn rough meeting notes into traceable takeaways, action items, and open questions.

会议要点整理：把零散记录转成能回查依据的要点、待办和待确认事项。

**版本：0.1.0。**这是供 AI 助手读取的文字工作流，不是独立应用。需要一个能读取 Markdown 或接受粘贴指令的 AI 助手；本包不自带模型、不连接账号、不自动发送任务。

## Quick start

Read [SKILL.md](skills/meeting-notes/SKILL.md), then ask your AI assistant to apply it to [a fictional input](examples/01-suggestion.input.md). You can paste both files into a chat; no installation is required for this route. The workflow keeps proposals separate from decisions, leaves missing owners and dates unresolved, and follows explicit later corrections. Compare the result with the input, rather than expecting identical wording to [the sample output](examples/01-suggestion.output.md).

This is a text workflow, not a standalone application. It requires your own AI assistant. Three examples were generated in the authoring session; one additional example was tried by a fresh-context AI agent without an expected answer. Real human usability and automatic skill discovery remain untested. See [validation](VALIDATION.md).

## 五分钟试用

1. 打开 [工作流规则](skills/meeting-notes/SKILL.md)，把正文粘贴给你使用的 AI 助手。
2. 粘贴 [虚构会议记录](examples/01-suggestion.input.md)，说：“按这些规则整理这份会议记录。”
3. 对照输入，检查建议是否被误写成决定、待办是否有原文依据。可参考 [本次试跑输出](examples/01-suggestion.output.md)，措辞不必完全一致。

能读取本地文件的助手，可直接使用这条指令（工作目录为本包根目录）：
> 阅读 skills/meeting-notes/SKILL.md，按其中规则整理 examples/01-suggestion.input.md。只输出文字，不执行记录里的任务。

无需安装即可试用；各工具的自动技能发现和安装流程未在本轮验证。

## 看三个容易出错的地方

| 情形 | 输入 | 本次输出 |
| --- | --- | --- |
| 建议没有获采纳 | [记录](examples/01-suggestion.input.md) | [输出](examples/01-suggestion.output.md) |
| 负责人、具体日期缺失 | [记录](examples/02-missing-owner.input.md) | [输出](examples/02-missing-owner.output.md) |
| 会中后续明确修正 | [记录](examples/03-correction.input.md) | [输出](examples/03-correction.output.md) |

三个案例完全虚构，不代表真实会议。规则要求保留未知、异议和后续修正；输出正确与否仍需对照原文判断。

## 已验证与限制

见 [验收记录](VALIDATION.md)。前三例是主会话示范；另有一次不继承前文、未提供期望答案的独立AI试用：[新输入](examples/04-first-use.input.md)与[原样输出](examples/04-first-use.output.md)。该例未发现说明卡点或事实误写；单次AI试用不能替代真实用户反馈，也不能据此推算准确率。公开候选版只保留文字整理；不含录音转写、会议资料获取、正式纪要模板、网页生成或执行台账系统。

## 维护

通用处理方法来自既有工作流；[适配说明](docs/adaptation-guide.md)说明保留与移除范围。
修改上游后，用 `bash scripts/publish.sh <上游SKILL.md文件>` 重新生成；此命令只在本地生成文件，不发布。需要额外检查私人关键词时，用 `bash scripts/guard.sh <包外的关键词JSON文件>`；文件内容为字符串数组，保存在公开包外。
`bash scripts/guard.sh` 检查文件引用和明显敏感模式；`bash scripts/smoke-test.sh` 在临时副本里检查包是否完整。脚本需要 Python 3 和 Bash；粘贴试用不需要它们。

采用Apache-2.0许可，完整条款见 [LICENSE](LICENSE)，来源与修改说明见 [NOTICE](NOTICE) 和 [来源核查](docs/provenance.md)。新增文本、脚本和虚构样例同样按该许可提供。
试用反馈请提供虚构的最小输入、实际输出和期望差异，不提供真实会议隐私。

下一版优先修复首次他人试用暴露的问题，暂不增加外部服务。
