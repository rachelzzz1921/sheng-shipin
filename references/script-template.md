# 分镜模板

一支片先填完这份表，再写成 `storyboard.json`。不要在这一步渲染。

## 核心洞察

用两句话写完。第一句是观众原以为的事。第二句是片子真正要翻过来的事。

## 叙事锚

这一支要什么主体，就写什么主体。不预设固定角色。代码画不好的人、动物、物件，写进下面的 `assets`，不要上网找图。

## 视觉反转

写明发生在第几镜、第几秒。观众必须在静帧里看出镜头拉远或空间变了，而不是只看到新字幕。

## 结尾

先选定一个，不要三个都拍：

- 锋利：一句判断，画面冷，不煽情
- 可截图：最后两行能单独当封面，定格约 2 秒
- 有人味：情绪重一点，仍然不出现消费升级

## 分镜表

总时长 88–90 秒。每一行一镜。

| 时间 | 字幕 | 主动作 | 画风 id | 动效 id | 是否反转 |
| --- | --- | --- | --- | --- | --- |
| 0–3s | 一句，最多两行 | 一个动作 | 见 styles.md | 见 prompt-motion.md | 否 |

画风 id 用花叔的场景 id，例如 `12_bauhaus`。动效 id 只用这些：`kinetic-type`、`shape-morph`、`spring`、`beat-hold`、`pull-back`。反转镜的动效必须是 `pull-back`。

## storyboard.json

```json
{
  "id": "短横线英文名",
  "title": "片名",
  "duration_s": 90,
  "source": "life-guide 或 essay",
  "life_guide": [],
  "insight": "第二句洞察",
  "ending": "sharp 或 screenshot 或 human",
  "assets": [
    {
      "file": "这一支的文件名.png",
      "subject": "这一张要画什么。只写主体和姿势，格式段由 prompts 命令补上。",
      "canvas": "1024×1024"
    }
  ],
  "beats": [
    {
      "id": "b01",
      "start_s": 0,
      "end_s": 3,
      "subtitle": "字幕",
      "action": "主动作",
      "style_id": "12_bauhaus",
      "motion": "kinetic-type",
      "reversal": false
    }
  ]
}
```

`life_guide` 只在内容来自人生指南时填写，每项是「第 N 节第 M 条」。爆文概念留空数组，并在 `insight` 里不要伪装成书里的原句。
