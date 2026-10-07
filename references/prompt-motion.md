# Prompt Motion 里采纳的动效

来源是 https://prompt-motion.com 。下面只收对 Rachel 有用的动效和提示词。作品集空话（「做一条 15 秒简历片，全力以赴」）在站上反复出现，不进入制作。提示词版权归各位作者，这里只作管线内部参考，并附原帖。

Rachel 把这些收成五种动效 id。分镜表的 `motion` 只能填其中之一。

## kinetic-type

大字本身在动：逐字进入，旧字退完新字才出现。

采纳自：

- [Bold kinetic type showreel](https://prompt-motion.com/shneural-2abdfa)（[@shneural](https://x.com/shneural)）只说明要做动态字，没有节拍。节拍以下面两条为准。
- [Orange dot motion system](https://prompt-motion.com/ultimaxbt-bbebf5)（[@ultimaxbt](https://x.com/ultimaxbt/status/2107486052550062398)）写明进出文字分开计时，字母不能重叠。

规则：每一拍有一次字的变化。出去的字和进来的字各有一段时间。不要把两句字幕叠在同一帧。

## shape-morph

换世界时不硬切。同一个形改大小、圆角和颜色，内容再换。

采纳自 [Shape morphing through UI states](https://prompt-motion.com/twoclipping-5cba86)（[@twoclipping](https://x.com/twoclipping/status/2103273003555402193)）。[Morphing UI states loop](https://prompt-motion.com/demonugc-4c5753) 是同一套说明。

原提示词里的制作约束，Rachel 照用：

- 每一帧只由时间 `t` 算出来，不用会在帧与帧之间残留的状态。
- 弹簧是过冲很小的闭合解。同一个值改了好几次目标，就叠加一次弹簧，仍然只取决于时间。
- 容器里的字要单独有进入和退出，否则会叠在一起。
- 镜头拉近时不要用会把字渲糊的办法。
- 先按节拍各出一帧，格子上站不住、挤、读不清的，先改再出全片。

原提示词要求 120 BPM、每拍都有事、最后一帧等于第一帧。Rachel 的成片不是循环广告，最后一帧改成定格约 2 秒，其余节拍要求保留。

## spring

数字或图表和带动它的那个点用同一个弹簧。点到了、图还没到，这镜打回。

采纳自上面的 orange dot 提示词：图和点必须是同一个运动，否则弹簧是假的。这里的「点」是这一支画面里的主体或一个小标记，不是橙色品牌点，结尾也不写别人的署名卡。

## beat-hold

这一镜故意慢，用来换气。仍然要有一个能看出来的变化，不能是静止贴图。静帧审查时要在备注里写出变化是什么。

## pull-back

反转专用。镜头拉开，观众看见她一直站在一个之前被裁掉的结构上。没有第二张「拉远之后」的静帧，闸门直接打回。

## 解说结构，不照搬商业五段

[Animated business explainer](https://prompt-motion.com/alex-prompter-1ea044)（[@alex_prompter](https://x.com/alex_prompter/status/2103499977632997524)）的原文是：30 秒、一个 HTML、五场，依次为问题、我做什么、三步怎么做、一个证据、名字。

Rachel 改成 88–90 秒，并且不出现品牌名和售卖。五段对应成：误解、一个世界里的说法、说法不够、视觉反转、选定的那句结尾。

[Recursion explained in genres](https://prompt-motion.com/emollick-8661a8)（[@emollick](https://x.com/emollick)）用完全不同的片种重复讲同一件事。Rachel 只借用「每个世界画风不同」，人物和洞察保持同一个。

[What is Git explainer](https://prompt-motion.com/yunn260414-60d996) 和 [Derivative concept explainer](https://prompt-motion.com/linearuncle-5d2bae) 要求把概念讲到零基础能懂。公式和坐标系不交给花叔场景，那一类改用 Manim。人生指南的事实仍以书的条目为准。

## 明确不采用的提示词

下面这些在站上能打开，但没有比上面更多的做法，制作时不要拿来当任务：

- [Motion principles showreel](https://prompt-motion.com/chatgptastra-0d95c7)：只有「用动态设计师的审美做 15 秒」。
- [Motion techniques showreel](https://prompt-motion.com/lukasersil-0ed38e)：列出了动能字、流体、粒子、变形、遮罩、光。粒子和与元素无关的变形在 Rachel 里禁止。其余已收进上面的 id。
- [Easing and morphing showreel](https://prompt-motion.com/roundtablespace-d3a1be)、[Type, form, space](https://prompt-motion.com/web3wesley-7bb108)、[Swiss-style](https://prompt-motion.com/levabashidze-2d713a)、[Keyframe motion design reel](https://prompt-motion.com/grace-sunnyy-29bc61)、[Overthinking motion study](https://prompt-motion.com/gizakdag-cf4ae6)：都是「做一条好看的 15 秒作品集」，没有可执行的节拍。
- [Deliberately terrible motion showreel](https://prompt-motion.com/henkpoley-3d3407)：原文要求做得尽量差、能少做就少做。审查时拿它当反例。看起来像交差，就打回。

站上其余条目大多是产品宣传片，不进入这套管线。
