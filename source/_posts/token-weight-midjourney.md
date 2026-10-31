早上好。最近，我一直在深入研究一件事。它既让我兴奋，也让我有些难过。不过和往常一样，我仍然愿意保持乐观。下面具体说说原因。

让我兴奋的是，接下来要分享的内容再次证明，创作中的灵感比以往任何时候都更重要。诗人、策展人，以及那些懂得精准用词的人，显然比一味堆砌技术术语、指望借此得到好结果的人更有优势。相机型号、焦距、ISO 等参数，对图像的影响其实已经很小，而且还在继续减弱。真正能改变画面的，是明确的创作意图、文化参照，以及找到模型中尚未被充分探索之处的能力。换句话说，就是走出所谓的“潜在空间高密度区”。顺便一提，这和卢克·天行者没有什么关系，至少据我所知没有。

这个现象并不新鲜。让我感到难过的是，Midjourney 正在以惊人的速度扩大它的潜在空间高密度区。每一轮新训练都会吸收更多图像，而这些图像的质量并不都很高。模型给出的“平均结果”越来越接近一个精致、通用，却十分乏味的中心地带。这个问题已经被讨论过很多次，而且几乎存在于每个领域：大多数人不断追随和堆叠流行趋势，真正出众的作品，则只会留给那些敢于打破常规、尝试创新、主动走出人群的创作者。

下面我会介绍自己的发现。不过先提醒一句，今天的内容会涉及一些技术细节。如果有些地方听起来难以理解，不必紧张。你只需要把握大意，再结合提示词和图片来看就可以了。

## 模型究竟如何理解你的提示词

我们先从基本机制说起：图像生成模型使用的是带有权重的 Token。这个权重代表了模型赋予你输入内容中各部分的数值大小；而在最终生成图像的概率分布中，各个数值彼此竞争。要理解这一点，我们需要简短地涉及一些技术概念。你可以选择现在停下来，或者去给自己倒一杯好咖啡。

图像生成模型包含一个潜在空间。这是一个高维数学空间，视觉概念与文本概念在其中共存。当你写下提示词时，每个词都会转化为该空间内的一个向量，也就是一个方向。模型会依据各个方向的相对权重将它们组合起来，以此决定生成怎样的图像。最终生效的提示词，正是这种组合后的结果。

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*_RjTO9vlnypZCIsHyzvVSQ.png)

Midjourney 于 2022 年 7 月 12 日上线。从 V1 到 V3 版本，它的风格充满创意与混沌感，同时也有很明显的局限。当时图像都是通过 Discord 生成的，这种方式如今依然可用；想要创建专属的私密频道，只需把机器人拉进自己的服务器即可。在 Discord 中，仍保留着若干网页端没有的指令，它们能为我们提供极有价值的参考，帮助我们看清模型如何处理权重。其中一个就是 `/shorten`。

`/shorten` 是一个提示词精简工具，它依据组成提示词的各个 Token 的权重显著性来工作。它主要为我们提供两项信息：一是模型赋予每个 Token 的权重，二是剔除对出图结果毫无影响的词之后得到的精简版提示词。需要明确的是，`/shorten` 展示的并不是模型内部真正的底层权重——那些数据在外部是无法获取的——而是估算各个 Token 对引导图像最终方向的贡献程度。这是一种近似估算，但正如我们随后会看到的，它的准确度已经足够高，具备切实的参考与预测价值。

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*9MQCwMXAnOsu6rfXUfdj1w.png)

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Fx2TfAotGhDvWCY2sN9nkg.png)

![](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*tVVMUfMnxOMC4hozJE76hA.png)

```text
Prompt 1) portrait of an elderly fisherman, weathered face, professional camera, studio lighting, high resolution
Results: portrait (0.01) elderly (0.11) fisherman (1.00) weathered (0.03) face (0.03) professional (0.00) camera (0.00) studio (0.01) lighting (0.00) high (0.00) resolution (0.00)
Prompt 2) portrait of an elderly fisherman, weathered face, Hasselblad 500CM, Kodak Portra 400, studio lighting
Results: portrait (0.01) elderly (0.12) fisherman (1.00) weathered (0.03) face (0.03) Hasselblad (0.00) 500CM (0.00) Kodak (0.01) Portra (0.01) 400 (0.00) studio (0.05) lighting (0.01)
Prompt 3) portrait of an elderly fisherman, weathered face, photograph by Steve McCurry, natural window light, analog film
Results: portrait (0.01) elderly (0.13) fisherman (1.00) weathered (0.03) face (0.06) photograph (0.00) Steve McCurry (0.21) natural (0.04) window (0.01) light (0.00) analog (0.01) film (0.01)
Prompt 4) portrait photography, 85mm lens, f1.4 aperture, ISO 200, golden hour, bokeh background, sharp focus
Results: portrait (1.00) photography (0.01) 85mm (0.14) lens (0.00) f1.4 (0.01) aperture (0.00) ISO (0.00) 200 (0.00) golden (0.01) hour (0.05) bokeh (0.04) background (0.01) sharp (0.01) focus (0.00)
Prompt 5) dramatic rim lighting, single source hard light, deep shadows, high contrast, chiaroscuro, black and white portrait
Results: dramatic (0.03) rim (0.03) lighting (0.22) single (0.01) source (0.02) hard (0.00) light (0.02) deep (0.01) shadows (0.04) high (0.00) contrast (0.01) chiaroscuro (0.01) black (0.01) white (0.02) portrait (1.00)
Prompt 6) Afghan girl with piercing green eyes, dramatic side lighting, National Geographic, Kodak film, Steve McCurry
Results: Afghan (0.25) girl (1.00) piercing (0.00) green (0.06) eyes (0.02) dramatic (0.01) side (0.00) lighting (0.01) National Geographic (0.01) Kodak (0.00) film (0.00) Steve McCurry (0.03)
Prompt 7) luxury perfume bottle product photography, reflective surface, gradient background, soft box lighting, commercial studio
Results: luxury (0.09) perfume (1.00) bottle (0.06) product (0.03) photography (0.21) reflective (0.12) surface (0.01) gradient (0.62) background (0.01) soft (0.25) box (0.01) lighting (0.02) commercial (0.00) studio (0.00)
Prompt 8) luxury perfume bottle, Nick Knight photography style, editorial fashion, specular highlights, Vogue magazine
Results: luxury (0.04) perfume (0.34) bottle (0.26) Nick Knight (1.00) photography (0.05) style (0.01) editorial (0.03) fashion (0.02) specular (0.02) highlights (0.02) Vogue (0.00) magazine (0.00)
Prompt 9) 35mm analog film portrait, grain texture, faded colors, light leaks, lomography, vintage 1970s photograph
Results: 35mm (0.22) analog (0.03) film (0.01) portrait (1.00) grain (0.00) texture (0.01) faded (0.02) colors (0.00) light leaks (0.12) lomography (0.02) vintage (0.03) 1970s (0.12) photograph (0.00)
Prompt 10) documentary street photography, Cartier-Bresson, decisive moment, candid portrait, studio lighting, posed, retouched
Results: documentary (0.03) street (0.33) photography (0.00) Cartier-Bresson (1.00) decisive (0.00) moment (0.04) candid (0.06) portrait (0.09) studio (0.08) lighting (0.03) posed (0.02) retouched (0.00)

```
