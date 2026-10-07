---
name: rachel
description: "通用短视频管线。每一支片子单独列素材，需要的图由用户按提示词在 ChatGPT 里生成透明 PNG，不搜网图。图交回并检查通过后才出静帧；静帧审查通过之前不准渲染 MP4。"
---

# Rachel

Rachel 是管线的名字，不是固定角色，也不绑定某一支剧本。用户这次要做什么视频，就做那一支。一次只做一支。学术研究套件不参与。

画面里要什么人、动物、物件，以这一支的分镜为准。代码画不好、本来会去网上找的图，改成 ChatGPT 透明 PNG。规格见 `references/gpt-image.md`。不要使用花叔仓库里的卡通形象。

## 先判断内容从哪来

- 用户给的是生活问题（该不该、值不值、能领什么、犯不犯法）：先按 `HowToLiveBetter/skills/life-decision-guide/SKILL.md` 从 `HowToLiveBetter/book/` 抽出条目。回答和字幕里的事实必须能指回第几节第几条。书里没有的句子标成「不是书里的」。
- 用户给的是一篇网络爆文或一个概念：用 `references/script-template.md` 收成脚本。不另写用户没有要求的成片故事。

## 制作顺序

未拿到用户对静帧的「通过」之前，禁止调用花叔 `render.py` 的整段出片（任何不带 `--stills` 的渲染）。

1. 锁定分镜。88–90 秒。每一镜只有一句字幕、一个主动作、一种画风、一种动效。最后一句留出约 2 秒定格。这一步只写 `storyboard.json`，不出图。
2. 在分镜的 `assets` 里列出这一支要贴进画面、代码画不好的图。人、动物、物件都写在这里，不预设固定角色。没有这种图就写空数组。禁止上网搜图。
3. 运行 `python3 scripts/gate.py prompts --storyboard <文件>`，把生成的 `reviews/<id>/生图提示词.md` 交给用户，然后停。用户在 ChatGPT 里生成后，按文件名存到 `assets/<id>/` 再发回。用 `python3 scripts/gate.py assets --storyboard <文件>` 确认都是带透明通道的 PNG。没到齐就不出静帧、不出视频。空的 `assets` 跳过这一步。
4. 只出静帧。运行 `python3 scripts/gate.py stills --storyboard <文件> --execute`。每一镜的起始时刻一张；标了反转的镜再加一张「拉远之后」。
5. 生成审查包。`python3 scripts/gate.py packet --storyboard <文件>`。检查员只看图，按 `references/keyframe-review.md` 打回，不改代码。
6. 把接触表交给用户。用户明确回复「通过」之后，把这个词写入 `reviews/<id>/APPROVED`。
7. 只有这时才允许 `python3 scripts/gate.py render --storyboard <文件> --execute`。配音和剪映字幕留在 MP4 之后。

## 画面从哪来

- 画风场景用花叔引擎，只读目录 `vendor/huashu-art-motion`。这里只检出了 `scripts/` 和 `references/`，没有示范视频。风格 id 以 `references/styles.md` 为准。表里标了缺失的，不要临时发明渲染器。
- 动效以 `references/prompt-motion.md` 为准：一个元素连续变形、节拍上有变化、进出文字不重叠、先出静帧再出片。来源是 https://prompt-motion.com ，提示词归原作者。

## 不许做的事

- 不要把三个仓库的结论写进同一次回答。
- 不要在审查通过前渲染 MP4。
- 不要用豪宅、名牌、金币雨表示「变好了」。
- 不要让反转只发生在字幕里。镜头必须真的拉开。
